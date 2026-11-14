"""Read-only combined inventory; never performs scheduling or acceptance mutations."""
from pathlib import Path
from iter_contracts import parse_card
from iter_preflight import _dispatch_check, dispatch_check


def inventory(directory, root, mode, context=None, phase='implementation', phase_from_context=False, details=False, phase_observer=None):
    from iter_queries import discover_task_files, audit_task_file, _render_task_envelope
    root, directory = Path(root).resolve(), Path(directory).resolve()
    if mode not in ('continue', 'takeover'):
        raise ValueError('Inventory mode must be continue or takeover')
    result = dict(version=1, read_only=True, mode=mode, readiness='NEEDS_INPUT', tasks=[], findings=[])
    if not directory.is_dir() or not directory.is_relative_to(root):
        result.update(readiness='BLOCKED', findings=['Iteration directory leaves/misses project'])
        return result
    cache = {}

    def audit(path):
        key = Path(path).resolve()
        if not key.is_relative_to(root):
            raise ValueError('Task card leaves project root')
        if key not in cache:
            cache[key] = audit_task_file(key)
        return cache[key]

    for card in discover_task_files(directory, read_root=root):
        row = dict(path=card.relative_to(root).as_posix(), task_id=card.stem, readiness='BLOCKED',
                   phase=None, findings=[], acceptance_verdict='UNKNOWN')
        try:
            if not card.resolve().is_relative_to(root):
                raise ValueError('Task card leaves project root')
            if phase_observer is not None:
                ready = _dispatch_check(card, root, context, phase, '', audit, False, phase_from_context, phase_observer)
            elif phase_from_context:
                ready = _dispatch_check(card, root, context, phase, '', audit, False, True)
            else:
                ready = dispatch_check(card, root, context, phase, '', audit, require_owner=False)
            envelope = _render_task_envelope(card, root, audit)
            if 'error' in envelope:
                raise ValueError('Handoff unavailable: '+str(envelope['error']))
            handoff = envelope['TASK_HANDOFF']
            execution = handoff['execution']
            last = execution.get('last_attempt') or {}
            row.update(task_id=handoff['task_id'], readiness=ready['readiness'], phase=ready['phase'],
                       findings=ready['findings'], status=handoff['status'], type=handoff['type'],
                       delivery_mode=handoff['delivery_mode'], candidate=ready.get('candidate'),
                       candidate_id=handoff['candidate_id'], commit_sha=handoff['commit_sha'],
                       review_status=handoff['review_status'], acceptance_verdict=handoff['acceptance_verdict'],
                       receipt=handoff['evidence']['receipt'], audit_findings=handoff['errors'],
                       writer=handoff['writer'], blocked_reason=handoff['blocked_reason'],
                       execution=dict(attempt_count=execution['attempt_count'], no_progress_streak=execution['no_progress_streak'],
                                      checkpoint=execution['checkpoint'], remaining_work=execution['remaining_work'],
                                      last_attempt_source=last.get('source')))
            if mode == 'takeover':
                meta, _, _ = parse_card(card.read_text(encoding='utf-8'))
                row['missing'] = [k for k in ('schema_version','type','task_id','review_receipt') if not meta.get(k)]
            if details:
                row['details'] = dict(preflight=ready, handoff=envelope['TASK_HANDOFF'])
        except (OSError, UnicodeError, ValueError, TypeError, KeyError, RuntimeError) as error:
            row['readiness'] = 'BLOCKED'
            row['acceptance_verdict'] = 'UNKNOWN'
            row['findings'].append(str(error))
            if mode == 'takeover': row['missing'] = None
        result['tasks'].append(row)
    if not result['tasks']:
        result['findings'].append('No tasks found; empty inventory is not READY')
    elif any(t['readiness'] == 'BLOCKED' for t in result['tasks']):
        result['readiness'] = 'BLOCKED'
    elif all(t['readiness'] == 'READY' for t in result['tasks']):
        result['readiness'] = 'READY'
    if mode == 'takeover':
        result['next'] = 'Request migration/reverification authorization where needed; preserve history'
    return result
