"""Optional session timing trace. Observations are not acceptance evidence."""
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from iter_contracts import relative_path, contained
from iter_execution import instant, interval, union_seconds

CATEGORIES = {'inventory', 'execution', 'verification', 'review', 'handoff', 'other'}


def now():
    return datetime.now(timezone.utc).isoformat()


def trace_path(root, name, exists=True):
    root = Path(root).resolve()
    path = (root / relative_path(str(name))).resolve()
    if not path.is_relative_to(root) or path == root:
        raise ValueError('Trace must be inside project root')
    if exists and not path.is_file():
        raise ValueError('Trace does not exist')
    return path


def initialize(root, name, session_id):
    if not isinstance(session_id, str) or not session_id.strip():
        raise ValueError('Session ID required')
    path = trace_path(root, name, False)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps({'type': 'trace', 'version': 1, 'session_id': session_id}, ensure_ascii=False)+'\n')


def read_trace(root, name):
    path = trace_path(root, name)
    lines = path.read_text(encoding='utf-8').splitlines()
    if not lines:
        raise ValueError('Empty timing trace')
    rows = [json.loads(line) for line in lines]
    header = rows[0]
    if (not isinstance(header, dict) or set(header) != {'type', 'version', 'session_id'}
            or header['type'] != 'trace' or type(header['version']) is not int or header['version'] != 1
            or not isinstance(header['session_id'], str) or not header['session_id'].strip()):
        raise ValueError('Invalid timing trace header')
    return header, rows[1:]


def append(root, name, row):
    read_trace(root, name)
    with trace_path(root, name).open('a', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(row, ensure_ascii=False, separators=(',', ':'))+'\n')
        stream.flush()
        os.fsync(stream.fileno())


def source_path(root, name):
    return contained(Path(root).resolve(), name).relative_to(Path(root).resolve()).as_posix()


def import_record(root, name, source):
    source = source_path(root, source)
    data = json.loads((Path(root).resolve()/source).read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('type') not in ('session', 'session_terminal', 'activity'):
        raise ValueError('Source must contain a session, session_terminal or activity observation')
    record = dict(data, source_kind='external', source=source)
    validate_record(record, root)
    if record['type'] == 'session_terminal' and record['session_id'] != read_trace(root, name)[0]['session_id']:
        raise ValueError('Terminal session ID differs from trace')
    append(root, name, record)


def import_receipt(root, name, source, category, operation, target):
    root = Path(root).resolve()
    source = source_path(root, source)
    receipt = json.loads((root/source).read_text(encoding='utf-8'))
    if (not isinstance(receipt, dict) or receipt.get('version') != 1
            or receipt.get('cwd') != str(root) or receipt.get('tree_terminal') is not True
            or receipt.get('status') not in ('COMPLETED', 'TIMED_OUT', 'NOT_STARTED', 'ERROR')):
        raise ValueError('Expected terminal runner receipt from this project')
    row = dict(type='activity', category=category, operation=operation, target=target,
               started_at=receipt.get('started_at'), ended_at=receipt.get('ended_at'),
               outcome=receipt['status'], raw_exit_code=receipt.get('raw_exit_code'),
               clock_basis='local_utc', source_kind='runner_receipt', source=source)
    validate_record(row, root)
    append(root, name, row)


def validate_record(row, root):
    if not isinstance(row, dict) or row.get('type') not in ('session', 'session_terminal', 'activity'):
        raise ValueError('Invalid timing record')
    if row.get('source_kind') not in ('external', 'runner_receipt', 'instrumented'):
        raise ValueError('Invalid timing source kind')
    if row['source_kind'] in ('external', 'runner_receipt'):
        # Historical trace keeps its source pointer even if later removed.
        source = relative_path(row.get('source', ''))
        if not (Path(root).resolve()/source).resolve().is_relative_to(Path(root).resolve()):
            raise ValueError('Source leaves project root')
    elif row.get('source') != 'trace':
        raise ValueError('Instrumented observation must refer to trace')
    basis = row.get('clock_basis')
    if basis is not None and (not isinstance(basis, str) or not basis.strip()):
        raise ValueError('Invalid clock basis')
    if row['type'] == 'session_terminal':
        if (row.get('source_kind') != 'external' or not isinstance(row.get('session_id'), str)
                or not row['session_id'].strip() or row.get('terminal_state') not in ('completed', 'failed', 'canceled')
                or row.get('ended_at') is None):
            raise ValueError('Terminal observation requires session ID, terminal state and end time')
    if row['type'] == 'activity':
        if row.get('category') not in CATEGORIES:
            raise ValueError('Invalid activity category')
        for key in ('operation', 'target'):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError('Activity requires operation and target')
    start, end = row.get('started_at'), row.get('ended_at')
    if start is not None:
        instant(start)
    if end is not None:
        instant(end)
    if start is not None and end is not None:
        return interval(start, end)
    return None


def report(root, name):
    header, rows = read_trace(root, name)
    activities, sessions, terminals, errors, source_rows = [], [], [], [], {}
    starts, finished, normalized = {}, set(), []
    for index, row in enumerate(rows, 2):
        if isinstance(row, dict) and row.get('type') == 'start':
            key = row.get('id')
            if not isinstance(key, str) or not key or key in starts:
                errors.append(f'line {index}: invalid or duplicate start ID')
            else:
                starts[key] = (index, dict(row, type='activity', ended_at=None))
        elif isinstance(row, dict) and row.get('type') == 'finish':
            key = row.get('id')
            if not isinstance(key, str) or key not in starts or key in finished:
                errors.append(f'line {index}: orphan or duplicate finish')
            else:
                starts[key][1].update(ended_at=row.get('ended_at'), outcome=row.get('outcome'),
                                      observed_phases=row.get('observed_phases', []))
                if 'phase_details' in row:
                    starts[key][1]['phase_details'] = row['phase_details']
                finished.add(key)
        else:
            normalized.append((index, row))
    normalized.extend(starts.values())
    for index, row in sorted(normalized):
        try:
            span = validate_record(row, root)
            if row.get('source_kind') in ('runner_receipt', 'external'):
                key = (row['source_kind'], row['source'])
                if key in source_rows:
                    if source_rows[key] != row:
                        errors.append(f'line {index}: conflicting source snapshot: {key[1]}')
                        activities = [(old, span) for old, span in activities if
                                      (old.get('source_kind'), old.get('source')) != key]
                        sessions = [(old, span) for old, span in sessions if
                                    (old.get('source_kind'), old.get('source')) != key]
                        terminals = [(old, span) for old, span in terminals if
                                     (old.get('source_kind'), old.get('source')) != key]
                    continue
                source_rows[key] = row
            if row['type'] == 'session_terminal' and row['session_id'] != header['session_id']:
                raise ValueError('Terminal session ID differs from trace')
            (sessions if row['type'] == 'session' else terminals if row['type'] == 'session_terminal' else activities).append((row, span))
        except (ValueError, TypeError, KeyError, OSError) as error:
            errors.append(f'line {index}: {error}')
    if len(sessions) > 1:
        errors.append('Multiple session observations; session boundary is ambiguous')
    session_row = sessions[0][0] if len(sessions) == 1 else None
    session = sessions[0][1] if len(sessions) == 1 else None
    if terminals:
        missing_source = False
        for row in ([session_row] if session_row else []) + [row for row, _ in terminals]:
            try:
                contained(Path(root).resolve(), row.get('source'))
            except (OSError, ValueError, TypeError):
                missing_source = True
        if missing_source:
            errors.append('Session or terminal observation source missing or unavailable')
        ends = {(instant(row['ended_at']), row.get('clock_basis'), row['terminal_state']) for row, _ in terminals}
        starts = {instant(row['started_at']) for row, _ in terminals if row.get('started_at') is not None}
        if len(ends) != 1 or len(starts) > 1:
            errors.append('Conflicting terminal observations')
            session = None
        elif session_row is not None:
            end, terminal_basis, _ = next(iter(ends))
            base = session_row.get('clock_basis')
            start = session_row.get('started_at')
            bad = (missing_source or session_row.get('session_id', header['session_id']) != header['session_id'] or
                   not base or terminal_basis != base or start is None or
                   any(row.get('started_at') is not None and instant(row['started_at']) != instant(start) for row, _ in terminals) or
                   (session_row.get('ended_at') is not None and instant(session_row['ended_at']) != end) or
                   (start is not None and end < instant(start)))
            if bad:
                errors.append('Session and terminal boundary or clock basis mismatch')
                session = None
            else:
                session = (instant(start), end)
                session_row = dict(session_row, ended_at=terminals[0][0]['ended_at'])
    spans = [span for _, span in activities if span is not None]
    basis = sessions[0][0].get('clock_basis') if len(sessions) == 1 else None
    comparable = bool(basis) and all(row.get('clock_basis') == basis for row, _ in activities)
    if session and comparable and any(start < session[0] or end > session[1] for start, end in spans):
        errors.append('Activity interval leaves session boundary')
    def comparable_rows(items):
        bases = [row.get('clock_basis') for row, span in items if span is not None]
        return not bases or (all(bases) and len(set(bases)) == 1)
    categories = {}
    for category in sorted(CATEGORIES):
        items = [(row, span) for row, span in activities if row['category'] == category]
        known = [span for _, span in items if span is not None]
        recorded_complete = len(items) == len(known) and not errors and comparable_rows(items)
        categories[category] = dict(count=len(items), known_count=len(known),
            known_resource_seconds=sum((end-start).total_seconds() for start, end in known),
            known_union_seconds=union_seconds(known) if comparable_rows(items) else None,
            complete=recorded_complete, recorded_intervals_complete=recorded_complete,
            full_activity_coverage='UNKNOWN')
    groups = defaultdict(list)
    for row, span in activities:
        if row['category'] == 'inventory':
            groups[(row['operation'], row['target'])].append(row)
    repeats = [dict(operation=key[0], target=key[1], calls=value)
               for key, value in sorted(groups.items()) if len(value) > 1]
    span_seconds = (max(s[1] for s in spans)-min(s[0] for s in spans)).total_seconds() if spans and comparable_rows(activities) else None
    covered = union_seconds(spans) if comparable_rows(activities) else None
    complete = session is not None and len(spans) == len(activities) and not errors and comparable
    result = dict(version=1, read_only=True, session_id=header['session_id'],
                session=session_row,
                session_seconds=(session[1]-session[0]).total_seconds() if session else None,
                activities=[row for row, _ in activities], categories=categories,
                clock_basis_comparable=comparable,
                observed_span_seconds=span_seconds, known_activity_union_seconds=covered,
                uncovered_seconds=(session[1]-session[0]).total_seconds()-covered if complete else None,
                repeated_inventory=repeats, errors=errors)
    if terminals:
        result['terminal_observations'] = [row for row, _ in terminals]
    return result
