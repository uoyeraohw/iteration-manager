import json
import subprocess
import sys
from pathlib import Path

import pytest

from test_execution_readiness import fixture

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/iter_sync.py'


def cli(root, *args):
    return subprocess.run([sys.executable, '-B', str(SCRIPT), *map(str, args)], cwd=root,
                          capture_output=True, encoding='utf-8')


def write(root, name, value):
    (root/name).write_text(json.dumps(value), encoding='utf-8')


def stamp(n):
    return f'2026-11-13T00:00:{n:02}+00:00'


def add(root, name, value):
    write(root, name, value)
    result = cli(root, '--timing-import', 'trace.jsonl', name)
    assert result.returncode == 0, result.stderr


def test_intervals_repeated_inventory_and_unknown_session(tmp_path):
    assert cli(tmp_path, '--timing-init', 'trace.jsonl', 'native-1').returncode == 0
    add(tmp_path, 'session.json', dict(type='session', clock_basis='local_utc', started_at=stamp(0), ended_at=stamp(20)))
    for i, (a,b,phase) in enumerate([(2,10,'implementation'), (5,15,'review')]):
        add(tmp_path, f'activity{i}.json', dict(type='activity', category='inventory', operation='preflight',
            target='docs/todos/01', requested_phase=phase, clock_basis='local_utc', started_at=stamp(a), ended_at=stamp(b)))
    before = (tmp_path/'trace.jsonl').read_bytes()
    p = cli(tmp_path, '--timing-report', 'trace.jsonl')
    assert p.returncode == 0, p.stderr
    data = json.loads(p.stdout)
    assert data['session_seconds'] == 20 and data['known_activity_union_seconds'] == 13
    assert data['categories']['inventory']['known_resource_seconds'] == 18
    assert data['uncovered_seconds'] == 7 and len(data['repeated_inventory'][0]['calls']) == 2
    assert (tmp_path/'trace.jsonl').read_bytes() == before
    add(tmp_path, 'missing.json', dict(type='activity', category='review', operation='review', target='01',
                                       started_at=stamp(15), ended_at=None))
    assert json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)['uncovered_seconds'] is None


def test_real_preflight_opt_in_and_old_call_unchanged(tmp_path):
    card, ctx, data = fixture(tmp_path)
    data['tasks']['01']['phase'] = 'evidence-inspection'
    write(tmp_path, ctx.name, data)
    original = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name)
    assert original.returncode == 3
    assert cli(tmp_path, '--timing-init', 'trace.jsonl', 'test-session').returncode == 0
    first = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name, '--timing-trace', 'trace.jsonl')
    second = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name, '--phase', 'evidence-inspection',
                 '--timing-trace', 'trace.jsonl')
    assert first.returncode == original.returncode and first.stdout == original.stdout
    assert second.returncode == 0
    result = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)
    calls = result['repeated_inventory'][0]['calls']
    assert [x['requested_phase'] for x in calls] == ['implementation', 'evidence-inspection']
    assert [x['outcome'] for x in calls] == ['BLOCKED', 'READY']
    assert all(x['context'] == ctx.name and x['owner'] == '' for x in calls)
    assert result['session_seconds'] is None and result['uncovered_seconds'] is None


def test_incomplete_conflicts_and_protected_trace(tmp_path):
    assert cli(tmp_path, '--timing-init', 'trace.jsonl', 'id').returncode == 0
    original = (tmp_path/'trace.jsonl').read_bytes()
    assert cli(tmp_path, '--timing-init', 'trace.jsonl', 'id').returncode != 0
    assert original == (tmp_path/'trace.jsonl').read_bytes()
    assert cli(tmp_path, '--timing-init', '../escape.jsonl', 'id').returncode != 0
    add(tmp_path, 's.json', dict(type='session', started_at=stamp(1), ended_at=stamp(10)))
    add(tmp_path, 's2.json', dict(type='session', started_at=stamp(1), ended_at=stamp(10)))
    p = cli(tmp_path, '--timing-report', 'trace.jsonl')
    assert p.returncode == 2 and json.loads(p.stdout)['uncovered_seconds'] is None


def test_interrupted_start_stays_unknown_and_orphan_finish_errors(tmp_path):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'id')
    row = dict(type='start', id='one', category='inventory', operation='preflight', target='01',
               source_kind='instrumented', source='trace', started_at=stamp(1))
    with (tmp_path/'trace.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(row)+'\n')
    result = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)
    assert result['activities'][0]['ended_at'] is None
    assert not result['categories']['inventory']['complete']
    with (tmp_path/'trace.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(dict(type='finish', id='different', ended_at=stamp(3)))+'\n')
    assert cli(tmp_path, '--timing-report', 'trace.jsonl').returncode == 2


def test_invalid_finish_and_repeat_external_source_are_safe(tmp_path):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'id')
    event = dict(type='activity', category='inventory', operation='preflight', target='01',
                 started_at=stamp(1), ended_at=stamp(2))
    add(tmp_path, 'one.json', event)
    assert cli(tmp_path, '--timing-import', 'trace.jsonl', 'one.json').returncode == 0
    result = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)
    assert result['categories']['inventory']['count'] == 1 and not result['repeated_inventory']
    with (tmp_path/'trace.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(dict(type='finish', id=[], ended_at=stamp(3)))+'\n')
    result = cli(tmp_path, '--timing-report', 'trace.jsonl')
    assert result.returncode == 2 and json.loads(result.stdout)['errors']


def test_different_or_unknown_clock_basis_never_produces_uncovered_time(tmp_path):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'id')
    add(tmp_path, 'session.json', dict(type='session', clock_basis='host-a', started_at=stamp(0), ended_at=stamp(20)))
    add(tmp_path, 'event.json', dict(type='activity', category='review', operation='review', target='01',
                                    clock_basis='host-b', started_at=stamp(2), ended_at=stamp(3)))
    result = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)
    assert result['clock_basis_comparable'] is False and result['uncovered_seconds'] is None
    add(tmp_path, 'other.json', dict(type='activity', category='review', operation='review', target='02',
                                    started_at=stamp(3), ended_at=stamp(4)))
    result = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)
    assert result['known_activity_union_seconds'] is None
    assert result['categories']['review']['known_union_seconds'] is None
    assert result['observed_span_seconds'] is None


def test_conflicting_external_source_snapshot_is_excluded(tmp_path):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'id')
    event = dict(type='activity', category='inventory', operation='preflight', target='01',
                 clock_basis='local_utc', started_at=stamp(1), ended_at=stamp(2))
    add(tmp_path, 'one.json', event)
    event['ended_at'] = stamp(3)
    add(tmp_path, 'one.json', event)
    result = cli(tmp_path, '--timing-report', 'trace.jsonl')
    data = json.loads(result.stdout)
    assert result.returncode == 2 and data['errors'] and not data['activities']


def test_inventory_trace_records_mode_and_context(tmp_path):
    card, ctx, _ = fixture(tmp_path)
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'id')
    result = cli(tmp_path, '--inventory', card.parent, '--mode', 'continue', '--context', ctx.name,
                 '--timing-trace', 'trace.jsonl')
    assert result.returncode == 0, result.stdout + result.stderr
    row = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)['activities'][0]
    assert row['mode'] == 'continue' and row['context'] == ctx.name and row['clock_basis'] == 'local_utc'


def test_real_runner_receipt_import(tmp_path):
    from datetime import datetime, timedelta, timezone
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'id')
    runner = SCRIPT.with_name('iter_run.py')
    deadline = (datetime.now(timezone.utc)+timedelta(seconds=30)).isoformat()
    p = subprocess.run([sys.executable, '-B', str(runner), '--deadline', deadline, '--evidence', 'receipt.json',
                        '--', sys.executable, '-c', 'print(42)'], cwd=tmp_path, capture_output=True)
    assert p.returncode == 0
    imported = cli(tmp_path, '--timing-import-receipt', 'trace.jsonl', 'receipt.json', '--category',
                   'verification', '--operation', 'test', '--target', '01')
    assert imported.returncode == 0, imported.stderr
    row = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)['activities'][0]
    receipt = json.loads((tmp_path/'receipt.json').read_text(encoding='utf-8'))
    assert row['started_at'] == receipt['started_at'] and row['ended_at'] == receipt['ended_at']
    assert row['source'] == 'receipt.json' and row['raw_exit_code'] == 0


@pytest.mark.parametrize('start,end', [(stamp(9),stamp(1)), ('2026-11-13T00:00:00',stamp(1))])
def test_rejects_invalid_external_timestamps(tmp_path, start, end):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'id')
    write(tmp_path, 'bad.json', dict(type='session', started_at=start, ended_at=end))
    assert cli(tmp_path, '--timing-import', 'trace.jsonl', 'bad.json').returncode != 0
