"""Attempt evidence snapshots and read-only summaries; no scheduler or acceptance."""
import json
from pathlib import Path
from datetime import datetime
from iter_contracts import contained, scope_paths, parse_card, relative_path
from iter_preflight import candidate_identity, execution_conditions, text, strings


def instant(value):
    stamp = datetime.fromisoformat(text(value, 'timestamp').replace('Z', '+00:00'))
    if stamp.utcoffset() is None:
        raise ValueError('Timestamp must include timezone')
    return stamp


def interval(start, end):
    if start is None and end is None:
        return None
    start, end = instant(start), instant(end)
    if end < start:
        raise ValueError('Timestamp interval reversed')
    return start, end


def union_seconds(intervals):
    if not intervals:
        return 0
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1] = merged[-1][0], max(end, merged[-1][1])
        else:
            merged.append((start, end))
    return sum((end-start).total_seconds() for start, end in merged)


def read_attempt(card, root, meta, content, evidence, executor_state):
    if executor_state not in ('completed', 'failed', 'canceled'):
        raise ValueError('Attempt requires queried terminal executor state')
    source = contained(root, evidence)
    data = json.loads(source.read_text(encoding='utf-8'))
    fields = {'version', 'phase', 'candidate', 'inputs', 'capabilities', 'checkpoint',
              'remaining_work', 'executor_id', 'terminal_evidence', 'progress', 'commands',
              'started_at', 'ended_at'}
    if not isinstance(data, dict) or set(data) != fields or type(data['version']) is not int or data['version'] != 1:
        raise ValueError('Invalid version:1 attempt report fields')
    mode, candidate = candidate_identity(card.resolve(), root, meta)
    if data['candidate'] != candidate:
        raise ValueError('Attempt candidate differs from actual project candidate')
    scope, errors = scope_paths(content)
    if errors:
        raise ValueError('; '.join(errors))
    terminal = contained(root, data['terminal_evidence']).relative_to(root).as_posix()
    progress = data['progress']
    if not isinstance(progress, list):
        raise ValueError('Attempt progress must be a list')
    normalized = []
    for item in progress:
        if not isinstance(item, dict) or set(item) != {'kind', 'evidence', 'summary'} or item['kind'] not in (
                'red', 'implementation', 'green', 'root-cause', 'review-finding'):
            raise ValueError('Invalid progress kind/fields')
        path = contained(root, item['evidence']).relative_to(root).as_posix()
        normalized.append(dict(kind=item['kind'], evidence=path, summary=text(item['summary'], 'progress summary')))
    spans, commands = [], []
    unknown_time = False
    for name in strings(data['commands'], 'commands', False):
        path = contained(root, name)
        receipt = json.loads(path.read_text(encoding='utf-8'))
        if (not isinstance(receipt, dict) or type(receipt.get('version')) is not int or receipt['version'] != 1
                or receipt.get('status') not in ('COMPLETED', 'TIMED_OUT', 'NOT_STARTED', 'ERROR')
                or receipt.get('tree_terminal') is not True
                or receipt.get('cwd') != str(root)
                or not isinstance(receipt.get('argv'), list) or not receipt['argv']
                or any(not isinstance(arg, str) or '\0' in arg for arg in receipt['argv'])
                or (receipt.get('raw_exit_code') is not None and type(receipt['raw_exit_code']) is not int)
                or (receipt['status'] == 'COMPLETED' and type(receipt.get('raw_exit_code')) is not int)):
            raise ValueError('Command requires project runner receipt and confirmed terminal process tree; COMPLETED needs raw exit')
        contained(root, receipt.get('output'), allow_empty=True)
        if receipt.get('started_at') is None and receipt['status'] in ('NOT_STARTED', 'ERROR'):
            if receipt.get('ended_at') is not None:
                instant(receipt['ended_at'])
            span = None
        else:
            span = interval(receipt.get('started_at'), receipt.get('ended_at'))
        if span is None:
            unknown_time = True
        else:
            spans.append(span)
        commands.append(dict(receipt=path.relative_to(root).as_posix(), status=receipt['status'], raw_exit_code=receipt.get('raw_exit_code'),
                             started_at=receipt.get('started_at'), ended_at=receipt.get('ended_at')))
    session = interval(data['started_at'], data['ended_at'])
    if session and any(start < session[0] or end > session[1] for start, end in spans):
        raise ValueError('Command interval leaves reported session')
    return dict(report=data, source=source.relative_to(root).as_posix(), phase=text(data['phase'], 'phase'),
                delivery_mode=mode, candidate=candidate, conditions=execution_conditions(data, root, scope),
                executor_id=text(data['executor_id'], 'executor_id'), executor_state=executor_state,
                terminal_evidence=terminal, progress=normalized,
                checkpoint=text(data['checkpoint'], 'checkpoint'),
                remaining_work=strings(data['remaining_work'], 'remaining_work', False), commands=commands,
                started_at=data['started_at'], ended_at=data['ended_at'],
                session_seconds=(session[1]-session[0]).total_seconds() if session else None,
                command_seconds=None if unknown_time or not commands else union_seconds(spans))


def execution_summary(state):
    """Insertion order is atomic event order, not user-supplied timestamps."""
    attempts, seen, streak, checkpoint = [], set(), 0, None
    for event in state['events'].values():
        payload = event.get('input', {})
        if payload.get('action') != 'attempt':
            continue
        attempt = payload['attempt']
        progress = attempt.get('progress', [])
        fresh = [item for item in progress if item['evidence'] not in seen]
        seen.update(item['evidence'] for item in progress)
        streak = 0 if fresh else streak + 1
        if fresh:
            checkpoint = dict(candidate=attempt.get('candidate'), phase=attempt['phase'],
                              summary=attempt['checkpoint'], progress=fresh, source=attempt.get('source'))
        attempts.append(attempt)
    return dict(attempt_count=len(attempts), no_progress_streak=streak,
                last_attempt={k:v for k,v in attempts[-1].items() if k != 'report'} if attempts else None, checkpoint=checkpoint,
                remaining_work=attempts[-1]['remaining_work'] if attempts else [])


def timing_totals(attempts, root, inventory_complete=True):
    """Aggregate historical snapshots, not today's mutable receipt files."""
    sessions, commands, conflicts, errors = {}, {}, set(), []

    def command_span(command):
        if command['started_at'] is None and command['status'] in ('NOT_STARTED', 'ERROR'):
            if command['ended_at'] is not None:
                instant(command['ended_at'])
            return None
        return interval(command['started_at'], command['ended_at'])

    def remember(records, key, value, kind):
        identity = (kind, key)
        if key in records and records[key] != value:
            conflicts.add(identity)
            errors.append('Conflicting '+kind+' snapshot: '+key)
        else:
            records[key] = value

    for attempt in attempts:
        session = dict(started_at=attempt['started_at'], ended_at=attempt['ended_at'])
        interval(session['started_at'], session['ended_at'])
        remember(sessions, text(attempt['executor_id'], 'executor_id'), session, 'session')
        for command in attempt['commands']:
            # Preserve historical identity even if an artifact has since been removed.
            name = relative_path(text(command['receipt'], 'receipt'))
            path = (root/name).resolve()
            if not path.is_relative_to(root):
                raise ValueError('Receipt leaves report project root')
            name = path.relative_to(root).as_posix()
            value = {k:command[k] for k in ('status', 'raw_exit_code', 'started_at', 'ended_at')}
            if (value['status'] not in ('COMPLETED', 'TIMED_OUT', 'NOT_STARTED', 'ERROR')
                    or (value['raw_exit_code'] is not None and type(value['raw_exit_code']) is not int)
                    or (value['status'] == 'COMPLETED' and type(value['raw_exit_code']) is not int)):
                raise ValueError('Invalid terminal command snapshot')
            command_span(value)
            remember(commands, name, value, 'command')
    timing, all_spans, complete = {}, [], inventory_complete and bool(attempts)
    for kind, records in (('session', sessions), ('command', commands)):
        spans, known, valid = [], 0, inventory_complete and bool(records)
        for key, record in records.items():
            if (kind, key) in conflicts:
                valid = False
                continue
            span = command_span(record) if kind == 'command' else interval(record['started_at'], record['ended_at'])
            if span is None:
                valid = False
            else:
                spans.append(span)
                known += (span[1]-span[0]).total_seconds()
        timing['known_'+kind+'_resource_seconds'] = known
        timing['known_'+kind+'_observed_union_seconds'] = union_seconds(spans)
        timing[kind+'_resource_seconds'] = known if valid else None
        timing[kind+'_observed_union_seconds'] = union_seconds(spans) if valid else None
        timing[kind+'_time_complete'] = valid
        complete = complete and valid
        all_spans.extend(spans)
    timing['complete'] = complete
    timing['observed_span_seconds'] = (max(s[1] for s in all_spans)-min(s[0] for s in all_spans)).total_seconds() if all_spans else None
    timing['iteration_elapsed_seconds'] = None  # No iteration lifecycle is recorded here.
    return dict(session_count=len(sessions), command_count=len(commands), timing=timing, errors=sorted(set(errors)))


def execution_report(directory, root):
    """Read-only task inventory. Missing or inconsistent history stays explicit."""
    from iter_autonomy import load_state
    from iter_queries import discover_task_files
    root, directory = Path(root).resolve(), Path(directory).resolve()
    if not directory.is_dir() or not directory.is_relative_to(root):
        raise ValueError('Report requires an iteration directory inside the current project root')
    tasks, attempts, errors, phases = [], [], [], {}
    for path in discover_task_files(directory, read_root=root):
        row = dict(path=path.relative_to(root).as_posix(), attempt_count=None, errors=[])
        try:
            if not path.resolve().is_relative_to(root):
                raise ValueError('Task card leaves report project root')
            meta, _, issues = parse_card(path.read_text(encoding='utf-8'))
            if issues:
                raise ValueError('; '.join(issues))
            state = load_state(meta)
            observed = []
            for event in state['events'].values():
                payload = event['input']
                if payload['action'] != 'attempt':
                    continue
                attempt = payload['attempt']
                if not isinstance(attempt, dict) or not isinstance(attempt.get('commands'), list):
                    raise ValueError('Invalid attempt snapshot/commands')
                text(attempt.get('phase'), 'phase')
                # Validate the whole card before merging it into global totals.
                timing_totals([attempt], root)
                observed.append(attempt)
            row.update(task_id=meta.get('task_id', path.stem), attempt_count=len(observed))
            row.update(timing_totals(observed, root))
            errors.extend(row['path']+': '+e for e in row['errors'])
            attempts.extend(observed)
            for attempt in observed:
                phases.setdefault(attempt['phase'], []).append(attempt)
        except (OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
            row['errors'] = [str(error)]
            errors.append(row['path']+': '+str(error))
        tasks.append(row)
    totals = timing_totals(attempts, root, not errors and all(row['attempt_count'] for row in tasks))
    errors.extend(totals.pop('errors'))
    return dict(version=1, read_only=True, task_count=len(tasks), attempt_count=len(attempts), tasks=tasks,
                **totals, errors=sorted(set(errors)),
                phases={name:dict(attempt_count=len(items), **timing_totals(items, root)) for name,items in sorted(phases.items())})
