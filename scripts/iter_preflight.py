"""Opt-in read-only dispatch readiness; never product acceptance or scheduling."""
import json
import subprocess
from pathlib import Path
from iter_contracts import parse_card, card_status, scope_paths, contained, TYPE_CHECKS
from iter_filesystem import load_profile


def text(value, name):
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError('Nonempty trimmed text required: '+name)
    return value


def strings(value, name, nonempty=True):
    if not isinstance(value, list) or (nonempty and not value):
        raise ValueError('List required: '+name)
    values = [text(item, name) for item in value]
    if len(values) != len(set(values)):
        raise ValueError('Duplicate value: '+name)
    return sorted(values)


def candidate_identity(card, root, meta):
    """Bind this explicit flow to its actual project and current candidate."""
    if not card.resolve().is_relative_to(root):
        raise ValueError('Task leaves project root')
    fs_root = load_profile(card.parent)
    if fs_root is not None:
        if fs_root != root or meta.get('delivery_mode') != 'filesystem':
            raise ValueError('Filesystem project/card identity mismatch')
        return 'filesystem', text(meta.get('candidate_id'), 'candidate_id')
    if meta.get('delivery_mode') == 'filesystem':
        raise ValueError('Filesystem card requires explicit valid delivery profile')
    if meta.get('delivery_mode', 'git') != 'git':
        raise ValueError('Unknown delivery mode; Git fallback is not allowed')
    proc = subprocess.run(['git', 'rev-parse', '--show-toplevel', 'HEAD'], cwd=root,
                          capture_output=True, text=True, encoding='utf-8', check=False)
    lines = proc.stdout.splitlines()
    if proc.returncode or len(lines) != 2 or Path(lines[0]).resolve() != root:
        raise ValueError('Run from the actual Git project root: '+proc.stderr.strip())
    return 'git', lines[1]


def read_context(root, path, task_id):
    data = json.loads(contained(root, path).read_text(encoding='utf-8'))
    if (not isinstance(data, dict) or set(data) != {'version', 'tasks'}
            or type(data['version']) is not int or data['version'] != 1 or not isinstance(data['tasks'], dict)):
        raise ValueError('Context requires version:1 and tasks object')
    context = data['tasks'].get(task_id)
    if not isinstance(context, dict):
        raise ValueError('Context missing task: '+task_id)
    allowed = {'phase', 'candidate', 'inputs', 'capabilities', 'dependencies', 'tool_entry',
               'checkpoint', 'remaining_work', 'observations', 'required_observations', 'change_evidence'}
    if set(context) - allowed:
        raise ValueError('Unknown execution context field')
    return context


def execution_conditions(context, root, scope):
    inputs = strings(context.get('inputs'), 'inputs')
    inputs = sorted({contained(root, item, allow_empty=True).relative_to(root).as_posix() for item in inputs})
    return dict(inputs=inputs, capabilities=strings(context.get('capabilities'), 'capabilities'), scope=sorted(scope))


def dispatch_check(card, root, context=None, phase='implementation', owner='', audit=None, require_owner=True):
    return _dispatch_check(card, root, context, phase, owner, audit, require_owner, False)


def _dispatch_check(card, root, context, phase, owner, audit, require_owner, phase_from_context, phase_observer=None):
    from iter_autonomy import load_state
    from iter_execution import execution_summary
    root, card = Path(root).resolve(), Path(card).resolve()
    result = dict(read_only=True, readiness='READY', task_path=str(card), phase=None if phase_from_context else phase,
                  acceptance_verdict='UNKNOWN', findings=[], observations={})
    context_phase = None

    def finding(status, message):
        result['findings'].append(message)
        if status == 'BLOCKED' or result['readiness'] == 'READY':
            result['readiness'] = status

    try:
        text(phase, 'phase')
        if not card.is_relative_to(root):
            raise ValueError('Task leaves project root')
        content = card.read_text(encoding='utf-8')
        meta, _, errors = parse_card(content)
        if errors:
            raise ValueError('; '.join(errors))
        task_id = text(meta.get('task_id'), 'task_id')
        if meta.get('type') not in TYPE_CHECKS:
            raise ValueError('Unknown task type; verification contract required')
        result['task_id'] = task_id
        result['delivery_mode'], result['candidate'] = candidate_identity(card, root, meta)
        scope, errors = scope_paths(content)
        if errors:
            raise ValueError('; '.join(errors))
        state = load_state(meta)
        execution = execution_summary(state)
        result['execution'] = execution
        status = card_status(content)
        if status in ('UNKNOWN', 'FUSED', 'DONE') or state.get('blocked_reason'):
            finding('BLOCKED', state.get('blocked_reason') or 'Task not dispatchable: '+status)
        if state['writer'] and owner and state['writer'] != owner:
            finding('BLOCKED', 'Task writer differs; confirm owner and native executor terminal state')
        if require_owner and (not owner or not state['writer']):
            finding('NEEDS_INPUT', 'Dispatch requires an already claimed current owner; preflight is inventory only')
        if not context:
            finding('NEEDS_INPUT', 'Explicit execution context and source observations required')
            return result
        ctx = read_context(root, context, task_id)
        try:
            context_phase = text(ctx.get('phase'), 'context phase')
        except ValueError:
            pass
        if phase_from_context:
            phase = text(ctx.get('phase'), 'context phase')
            result['phase'] = phase
        if ctx.get('phase') != phase or ctx.get('candidate') != result['candidate']:
            finding('BLOCKED', 'Context phase/candidate does not match current dispatch')
            if ctx.get('phase') != phase:
                finding('BLOCKED', f"Context phase mismatch: requested={phase!r}, context={ctx.get('phase')!r}")
            if ctx.get('candidate') != result['candidate']:
                finding('BLOCKED', f"Context candidate mismatch: actual={result['candidate']!r}, context={ctx.get('candidate')!r}")
            return result
        conditions = execution_conditions(ctx, root, scope)
        if execution['no_progress_streak'] >= 2:
            if conditions == execution['last_attempt']['conditions']:
                finding('BLOCKED', 'Two attempts without new progress; identical redispatch prohibited')
            elif not ctx.get('change_evidence'):
                finding('NEEDS_INPUT', 'Changed execution conditions require change_evidence')
            else:
                contained(root, ctx['change_evidence'])
        result.update(conditions=conditions, checkpoint=text(ctx.get('checkpoint'), 'checkpoint'),
                      remaining_work=strings(ctx.get('remaining_work'), 'remaining_work', False))
        entry = Path(text(ctx.get('tool_entry'), 'tool_entry'))
        if not entry.is_absolute() or entry.resolve() != Path(__file__).with_name('iter_sync.py').resolve() or not entry.is_file():
            raise ValueError('Execution context must name the actual invoked tool entry')
        required = {'authority', 'execution', 'verification'}
        if meta.get('type') == 'UI-Component':
            required.add('ui-entry')
        required.update(strings(ctx.get('required_observations', []), 'required_observations', False))
        observations = ctx.get('observations')
        if not isinstance(observations, dict):
            raise ValueError('Observed readiness facts required')
        for name in sorted(required):
            observation = observations.get(name)
            if not isinstance(observation, dict):
                finding('NEEDS_INPUT', 'Missing observation: '+name)
                continue
            value = observation.get('status')
            if value not in ('READY', 'NEEDS_INPUT', 'BLOCKED'):
                raise ValueError('Invalid observation status: '+name)
            text(observation.get('summary'), 'observation summary')
            if value == 'READY':
                contained(root, observation.get('evidence'))
            else:
                finding(value, name+': '+observation['summary'])
            result['observations'][name] = observation
        for dep in strings(ctx.get('dependencies'), 'dependencies', False):
            dependency = contained(root, dep)
            if dependency == card or audit is None or not audit(dependency)['is_valid_done']:
                finding('BLOCKED', 'Dependency has no valid completion evidence: '+dep)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
        finding('BLOCKED', str(error))
    finally:
        if phase_observer is not None:
            checked = result['phase']
            phase_observer.append(dict(task_path=str(card), task_id=result.get('task_id'),
                                       checked_phase=checked, context_phase=context_phase,
                                       phase_match=(checked == context_phase) if context_phase is not None and checked is not None else None))
    return result


def preflight(directory, root, context=None, phase='implementation', owner='', audit=None):
    return _preflight(directory, root, context, phase, owner, audit, False)


def preflight_from_context(directory, root, context=None, owner='', audit=None):
    return _preflight(directory, root, context, 'implementation', owner, audit, True)


def _preflight(directory, root, context, phase, owner, audit, phase_from_context, phase_observer=None):
    from iter_sync import discover_task_files
    directory, root = Path(directory).resolve(), Path(root).resolve()
    if not directory.is_dir() or not directory.is_relative_to(root):
        return dict(read_only=True, readiness='BLOCKED', tasks=[], findings=['Iteration directory leaves/misses project'])
    if phase_from_context and phase_observer is None:
        tasks = [_dispatch_check(card, root, context, phase, owner, audit, False, True)
                 for card in discover_task_files(directory, read_root=root)]
    elif phase_from_context:
        tasks = [_dispatch_check(card, root, context, phase, owner, audit, False, True, phase_observer)
                 for card in discover_task_files(directory, read_root=root)]
    elif phase_observer is None:
        tasks = [dispatch_check(card, root, context, phase, owner, audit, require_owner=False)
                 for card in discover_task_files(directory, read_root=root)]
    else:
        tasks = [_dispatch_check(card, root, context, phase, owner, audit, False, False, phase_observer)
                 for card in discover_task_files(directory, read_root=root)]
    readiness = 'BLOCKED' if any(t['readiness'] == 'BLOCKED' for t in tasks) else (
        'NEEDS_INPUT' if not tasks or any(t['readiness'] == 'NEEDS_INPUT' for t in tasks) else 'READY')
    return dict(read_only=True, readiness=readiness, tasks=tasks,
                findings=[] if tasks else ['No tasks found; empty inventory is not READY'])
