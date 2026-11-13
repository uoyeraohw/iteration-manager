import json
import pytest
from test_session_timing import cli, write, stamp
from test_execution_readiness import fixture


def test_terminal_append_preserves_start_source_and_completes_session(tmp_path):
    assert cli(tmp_path, '--timing-init', 'trace.jsonl', 'native-1').returncode == 0
    write(tmp_path, 'start.json', dict(type='session', clock_basis='local_utc', started_at=stamp(0), ended_at=None))
    assert cli(tmp_path, '--timing-import', 'trace.jsonl', 'start.json').returncode == 0
    write(tmp_path, 'end.json', dict(type='session_terminal', session_id='native-1', clock_basis='local_utc',
                                    started_at=stamp(0), ended_at=stamp(20), terminal_state='completed'))
    result = cli(tmp_path, '--timing-import', 'trace.jsonl', 'end.json')
    assert result.returncode == 0, result.stderr
    data = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)
    assert data['session_seconds'] == 20 and data['uncovered_seconds'] == 20
    assert data['session']['source'] == 'start.json' and data['terminal_observations'][0]['source'] == 'end.json'


def test_trace_captures_context_phase_during_preflight_not_from_later_file(tmp_path):
    card, ctx, data = fixture(tmp_path)
    data['tasks']['01']['phase'] = 'evidence-inspection'; write(tmp_path, ctx.name, data)
    assert cli(tmp_path, '--timing-init', 'trace.jsonl', 'test').returncode == 0
    before = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name)
    traced = cli(tmp_path, '--preflight', card.parent, '--context', ctx.name, '--timing-trace', 'trace.jsonl')
    assert traced.stdout == before.stdout and traced.returncode == before.returncode == 3
    data['tasks']['01']['phase'] = 'review'; write(tmp_path, ctx.name, data)
    activity = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)['activities'][0]
    assert activity['phase_details'][0]['checked_phase'] == 'implementation'
    assert activity['phase_details'][0]['context_phase'] == 'evidence-inspection'
    assert activity['phase_details'][0]['phase_match'] is False


@pytest.mark.parametrize('change', ['id', 'clock', 'start', 'reverse', 'state', 'missing_end'])
def test_terminal_bad_identity_boundary_or_clock_never_completes(tmp_path, change):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'native-1')
    write(tmp_path, 'start.json', dict(type='session', clock_basis='local_utc', started_at=stamp(5), ended_at=None))
    assert cli(tmp_path, '--timing-import', 'trace.jsonl', 'start.json').returncode == 0
    terminal = dict(type='session_terminal', session_id='native-1', clock_basis='local_utc',
                    started_at=stamp(5), ended_at=stamp(20), terminal_state='completed')
    if change == 'id': terminal['session_id'] = 'other'
    if change == 'clock': terminal['clock_basis'] = 'host-b'
    if change == 'start': terminal['started_at'] = stamp(4)
    if change == 'reverse': terminal['ended_at'] = stamp(3)
    if change == 'state': terminal['terminal_state'] = 'running'
    if change == 'missing_end': terminal['ended_at'] = None
    write(tmp_path, 'end.json', terminal)
    imported = cli(tmp_path, '--timing-import', 'trace.jsonl', 'end.json')
    report = cli(tmp_path, '--timing-report', 'trace.jsonl')
    assert json.loads(report.stdout)['session_seconds'] is None
    if imported.returncode == 0:
        assert report.returncode == 2 and json.loads(report.stdout)['errors']
    else:
        assert report.returncode == 0


def test_terminal_duplicates_and_conflicts_preserve_original_source(tmp_path):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'native-1')
    write(tmp_path, 'start.json', dict(type='session', clock_basis='local_utc', started_at=stamp(0), ended_at=None))
    cli(tmp_path, '--timing-import', 'trace.jsonl', 'start.json')
    terminal = dict(type='session_terminal', session_id='native-1', clock_basis='local_utc',
                    started_at=stamp(0), ended_at=stamp(20), terminal_state='completed')
    write(tmp_path, 'end.json', terminal)
    assert cli(tmp_path, '--timing-import', 'trace.jsonl', 'end.json').returncode == 0
    assert cli(tmp_path, '--timing-import', 'trace.jsonl', 'end.json').returncode == 0
    report = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)
    assert report['session_seconds'] == 20 and len(report['terminal_observations']) == 1
    write(tmp_path, 'end2.json', dict(terminal, ended_at=stamp(21)))
    cli(tmp_path, '--timing-import', 'trace.jsonl', 'end2.json')
    p = cli(tmp_path, '--timing-report', 'trace.jsonl')
    assert p.returncode == 2 and json.loads(p.stdout)['session_seconds'] is None
    assert json.loads((tmp_path/'start.json').read_text())['ended_at'] is None


def test_start_identity_mismatch_and_missing_source_fail_closed(tmp_path):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'native-1')
    write(tmp_path, 'start.json', dict(type='session', session_id='wrong', clock_basis='local_utc', started_at=stamp(0), ended_at=None))
    cli(tmp_path, '--timing-import', 'trace.jsonl', 'start.json')
    write(tmp_path, 'end.json', dict(type='session_terminal', session_id='native-1', clock_basis='local_utc',
                                    started_at=stamp(0), ended_at=stamp(20), terminal_state='completed'))
    cli(tmp_path, '--timing-import', 'trace.jsonl', 'end.json')
    p = cli(tmp_path, '--timing-report', 'trace.jsonl')
    assert p.returncode == 2 and json.loads(p.stdout)['session_seconds'] is None


@pytest.mark.parametrize('missing', ['start.json', 'end.json'])
def test_removed_observation_source_invalidates_merged_time(tmp_path, missing):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'native-1')
    write(tmp_path, 'start.json', dict(type='session', clock_basis='local_utc', started_at=stamp(0), ended_at=None))
    write(tmp_path, 'end.json', dict(type='session_terminal', session_id='native-1', clock_basis='local_utc',
                                    started_at=stamp(0), ended_at=stamp(20), terminal_state='completed'))
    cli(tmp_path, '--timing-import', 'trace.jsonl', 'start.json')
    cli(tmp_path, '--timing-import', 'trace.jsonl', 'end.json')
    (tmp_path/missing).unlink()
    p = cli(tmp_path, '--timing-report', 'trace.jsonl')
    assert p.returncode == 2 and json.loads(p.stdout)['session_seconds'] is None
    assert any('source missing' in e for e in json.loads(p.stdout)['errors'])


def test_conflicting_terminal_starts_without_session_are_reported(tmp_path):
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'native-1')
    terminal = dict(type='session_terminal', session_id='native-1', clock_basis='local_utc',
                    started_at=stamp(0), ended_at=stamp(20), terminal_state='completed')
    write(tmp_path, 'end.json', terminal); cli(tmp_path, '--timing-import', 'trace.jsonl', 'end.json')
    write(tmp_path, 'end2.json', dict(terminal, started_at=stamp(1))); cli(tmp_path, '--timing-import', 'trace.jsonl', 'end2.json')
    p = cli(tmp_path, '--timing-report', 'trace.jsonl')
    assert p.returncode == 2 and json.loads(p.stdout)['session_seconds'] is None


@pytest.mark.parametrize('mode', ['explicit', 'inferred', 'missing'])
def test_inventory_captures_per_card_context_without_changing_output(tmp_path, mode):
    card, ctx, data = fixture(tmp_path)
    second = card.with_name('02-task.md')
    second.write_text(card.read_text(encoding='utf-8').replace('task_id: "01"', 'task_id: "02"'), encoding='utf-8')
    data['tasks']['02'] = json.loads(json.dumps(data['tasks']['01']))
    data['tasks']['01']['phase'], data['tasks']['02']['phase'] = 'review', 'implementation'
    write(tmp_path, ctx.name, data)
    cli(tmp_path, '--timing-init', 'trace.jsonl', 'test')
    args = ['--inventory', card.parent, '--mode', 'continue']
    if mode != 'missing': args += ['--context', ctx.name]
    if mode == 'inferred': args += ['--phase-from-context']
    old = cli(tmp_path, *args); traced = cli(tmp_path, *args, '--timing-trace', 'trace.jsonl')
    assert (old.returncode, old.stdout) == (traced.returncode, traced.stdout)
    rows = json.loads(cli(tmp_path, '--timing-report', 'trace.jsonl').stdout)['activities'][0]['phase_details']
    assert [row['context_phase'] for row in rows] == ([None, None] if mode == 'missing' else ['review', 'implementation'])
    assert [row['phase_match'] for row in rows] == ([None, None] if mode == 'missing' else [True, True] if mode == 'inferred' else [False, True])
