"""Task-local persistent budgets. No scheduling, implicit reset or Git writes."""
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from iter_contracts import parse_card, card_status, contained

DEFAULT_POLICY = dict(round_limit=5, total_limit=10, consilium_limit=1, replan_limit=2)


def number(value, name):
    if isinstance(value, bool) or not re.fullmatch(r'\d+', str(value)):
        raise ValueError(f'Invalid nonnegative integer: {name}')
    return int(value)


def load_state(meta):
    policy = {**DEFAULT_POLICY, **json.loads(meta.get('autonomy_policy') or '{}')}
    if set(policy) != set(DEFAULT_POLICY):
        raise ValueError('Unknown autonomy policy field')
    policy = {k: number(v, k) for k, v in policy.items()}
    if min(policy.values()) < 1:
        raise ValueError('Autonomy limits must be positive')
    if meta.get('autonomy_state'):
        state = json.loads(meta['autonomy_state'])
        if not isinstance(state, dict) or state.get('version') != 1 or state.get('policy') != policy:
            raise ValueError('Invalid autonomy state or changed policy; explicit migration required')
    else:
        rounds = number(meta.get('fix_rounds', 0), 'fix_rounds')
        state = dict(version=1, policy=policy, round=rounds,
                     total=max(rounds, number(meta.get('fix_total', rounds), 'fix_total')),
                     consilium=number(meta.get('consilium_count', 0), 'consilium_count'),
                     replan=number(meta.get('replan_count', 0), 'replan_count'),
                     writer='', events={}, blocked_reason=meta.get('blocked_reason',''))
    for name in ('round', 'total', 'consilium', 'replan'):
        state[name] = number(state.get(name), name)
    if state['total'] < state['round'] or not isinstance(state.get('events'), dict) or not isinstance(state.get('writer'), str):
        raise ValueError('Invalid autonomy counters/events/writer')
    if state['total'] >= policy['total_limit']:
        state['blocked_reason'] = 'total repair budget exhausted'
    elif state['round'] >= policy['round_limit'] and not state.get('blocked_reason'):
        state['blocked_reason'] = 'round repair budget exhausted; bounded diagnosis/replan required'
    return state


def update_meta(content, changes):
    meta, _, errors = parse_card(content)
    if errors:
        raise ValueError('; '.join(errors))
    match = re.match(r'\A\ufeff?---[^\S\n]*\n(.*?)\n---[^\S\n]*(?:\n|$)', content, re.S)
    lines = match.group(1).splitlines()
    for key, value in changes.items():
        line = key + ': ' + json.dumps(value, ensure_ascii=False)
        index = next((i for i, x in enumerate(lines) if x.startswith(key+':')), None)
        if index is None:
            lines.append(line)
        else:
            lines[index] = line
    return '---\n'+'\n'.join(lines)+'\n---\n'+content[match.end():]


def record_event(task_file, action, event_id, owner, reason='', evidence='', executor_state='', resume_grant=None):
    """Atomic idempotent mutation; the caller must query executor state before recovery."""
    task_file = Path(task_file)
    lock = task_file.with_name(task_file.name+'.iter.lock')
    fd = None
    temp = None
    try:
        if not event_id or not owner:
            raise ValueError('Stable event_id and owner required')
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        content = task_file.read_text(encoding='utf-8')
        meta, _, errors = parse_card(content)
        if errors:
            raise ValueError('; '.join(errors))
        if card_status(content) == 'UNKNOWN':
            raise ValueError('Unknown task status; authorized migration required before mutation')
        state = load_state(meta)
        payload = dict(action=action, owner=owner, reason=reason, evidence=evidence, executor_state=executor_state)
        if action == 'resume-checkpoint':
            from iter_checkpoint import read_grant
            payload['resume_grant'] = read_grant(resume_grant)
        elif resume_grant is not None:
            raise ValueError('Resume grant only applies to resume-checkpoint')
        if event_id in state['events']:
            old = state['events'][event_id]
            if old['input'] != payload:
                raise ValueError('Event ID reused with different payload')
            return {**old['result'], 'replayed': True}
        if card_status(content) == 'DONE':
            raise ValueError('DONE is terminal; do not resume or rewrite accepted tasks')
        if action == 'resume-checkpoint':
            from iter_checkpoint import validate_resume
            validate_resume(task_file, state, card_status(content), payload['resume_grant'])
        if state['writer'] and state['writer'] != owner:
            raise ValueError('Task has another writer: '+state['writer'])
        if not state['writer']:
            state['writer'] = owner
        policy = state['policy']
        blocked = ''
        status = card_status(content)
        if action == 'resume-checkpoint':
            status = 'IN_PROGRESS'
        elif (action not in ('recover', 'release', 'closeout') and state.get('blocked_reason')
                and (action in ('claim', 'fix') or state['blocked_reason'] in
                     ('replan budget exhausted', 'consilium budget exhausted', 'total repair budget exhausted'))):
            blocked = state['blocked_reason']
        elif action == 'fix':
            if state['total'] >= policy['total_limit']:
                blocked = 'total repair budget exhausted'
            elif state['round'] >= policy['round_limit']:
                blocked = 'round repair budget exhausted; bounded diagnosis/replan required'
            else:
                state['round'] += 1
                state['total'] += 1
                if state['total'] >= policy['total_limit']:
                    blocked = 'total repair budget exhausted'
                elif state['round'] >= policy['round_limit']:
                    blocked = 'round repair budget exhausted; bounded diagnosis/replan required'
        elif action in ('consilium', 'replan'):
            if not reason or not evidence:
                raise ValueError('Diagnosis/replan requires reason and evidence reference')
            key = action+'_limit'
            if state['total'] >= policy['total_limit']:
                blocked = 'total repair budget exhausted'
            elif state[action] >= policy[key]:
                blocked = action+' budget exhausted'
            else:
                state[action] += 1
                if action == 'replan':
                    state['round'] = 0
                    status = 'IN_PROGRESS'
                else:
                    blocked = state.get('blocked_reason', '')
        elif action == 'closeout':
            if executor_state not in ('completed', 'failed', 'canceled') or not reason.strip() or not evidence:
                raise ValueError('Closeout requires queried terminal executor state, reason and evidence')
            contained(Path.cwd().resolve(), evidence)
            blocked = state.get('blocked_reason') or reason
            state['writer'] = ''
        elif action == 'recover':
            if executor_state not in ('completed', 'failed', 'canceled') or not evidence:
                raise ValueError('Recovery requires queried terminal executor state and evidence')
            blocked = state.get('blocked_reason', '')
        elif action == 'release':
            if executor_state not in ('completed', 'failed', 'canceled') or not evidence:
                raise ValueError('Release requires terminal executor evidence')
            state['writer'] = ''
            blocked = state.get('blocked_reason', '')
        elif action != 'claim':
            raise ValueError('Unknown autonomy action: '+action)
        else:
            blocked = state.get('blocked_reason', '')
        if blocked:
            status = 'FUSED'
        state['blocked_reason'] = blocked
        result = dict(task_id=task_file.stem, previous_rounds=number(meta.get('fix_rounds', 0), 'fix_rounds'),
                      current_rounds=state['round'], fix_total=state['total'], consilium_count=state['consilium'],
                      replan_count=state['replan'], is_fused=bool(blocked), status=status,
                      blocked_reason=blocked, writer=state['writer'], consilium_bundle=None)
        state['events'][event_id] = dict(input=payload, result=result, at=datetime.now(timezone.utc).isoformat())
        changed = update_meta(content, dict(autonomy_state=json.dumps(state, ensure_ascii=False, separators=(',', ':')),
                             fix_rounds=state['round'], status=status, is_blocked=bool(blocked),
                             blocked_reason=blocked, updated_at=datetime.now(timezone.utc).isoformat()))
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=task_file.parent, delete=False) as f:
            temp = f.name
            f.write(changed)
        os.replace(temp, task_file)
        temp = None
        return result
    except (OSError, ValueError, TypeError, KeyError) as error:
        return {'error': str(error), 'is_fused': True, 'status': 'BLOCKED'}
    finally:
        if temp:
            Path(temp).unlink(missing_ok=True)
        if fd is not None:
            os.close(fd)
            lock.unlink(missing_ok=True)
