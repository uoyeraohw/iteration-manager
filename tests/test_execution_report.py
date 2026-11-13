"""Report uses persisted observations, never re-executes commands or grants acceptance."""
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from iter_autonomy import load_state, update_meta

SCRIPT = Path(__file__).resolve().parents[1]/'scripts/iter_sync.py'


def stamp(second):
    return f'2026-11-12T00:00:{second:02d}+00:00'


def attempt(executor='a', start=0, end=20, command='receipt.json', phase='verification'):
    return dict(executor_id=executor, phase=phase, started_at=stamp(start), ended_at=stamp(end),
                commands=[dict(receipt=command, status='COMPLETED', raw_exit_code=0,
                               started_at=stamp(5), ended_at=stamp(15))])


def card(directory, name, attempts):
    directory.mkdir(parents=True, exist_ok=True)
    content = f'---\nstatus: TESTING\ntask_id: "{name}"\n---\n# Task\n'
    state = load_state({})
    for i, data in enumerate(attempts):
        state['events'][str(i)] = dict(input=dict(action='attempt', attempt=data))
    path = directory/f'{name}-task.md'
    path.write_text(update_meta(content, dict(autonomy_state=json.dumps(state))), encoding='utf-8')
    return path


def run(root, directory):
    before = {str(p):p.read_bytes() for p in root.rglob('*') if p.is_file()}
    proc = subprocess.run([sys.executable, '-B', str(SCRIPT), '--execution-report', str(directory)],
                          cwd=root, capture_output=True, encoding='utf-8')
    assert before == {str(p):p.read_bytes() for p in root.rglob('*') if p.is_file()}
    return proc


def test_report_deduplicates_and_separates_parallel_wall_and_resource_time(tmp_path):
    directory = tmp_path/'docs/todos/01-demo'
    original = attempt()
    card(directory, '01', [original, original])
    second = attempt('b', 10, 30, 'other.json', 'review')
    second['commands'][0].update(started_at=stamp(10), ended_at=stamp(20))
    card(directory, '02', [second, original])  # shared receipt and session across cards
    proc = run(tmp_path, directory)
    assert proc.returncode == 0, proc.stdout+proc.stderr
    data = json.loads(proc.stdout)
    assert data['read_only'] is True and data['attempt_count'] == 4
    assert data['session_count'] == data['command_count'] == 2
    assert data['timing']['session_resource_seconds'] == 40
    assert data['timing']['session_observed_union_seconds'] == 30
    assert data['timing']['command_resource_seconds'] == 20
    assert data['timing']['command_observed_union_seconds'] == 15
    assert data['timing']['iteration_elapsed_seconds'] is None
    assert data['timing']['observed_span_seconds'] == 30
    assert data['phases']['review']['attempt_count'] == 1
    assert 'acceptance_verdict' not in data


def test_legacy_empty_unknown_and_bad_card_remain_in_inventory(tmp_path):
    directory = tmp_path/'docs/todos/01-demo'
    card(directory, '01', [])
    unknown = attempt(); unknown.update(started_at=None, ended_at=None)
    unknown['commands'][0].update(started_at=None, ended_at=None)
    card(directory, '02', [unknown])
    (directory/'03-bad.md').write_text('---\nstatus: TODO\nautonomy_state: "{bad"\n---\n', encoding='utf-8')
    proc = run(tmp_path, directory)
    assert proc.returncode == 2, proc.stdout+proc.stderr
    data = json.loads(proc.stdout)
    assert data['task_count'] == 3 and len(data['tasks']) == 3
    assert data['tasks'][0]['attempt_count'] == 0
    assert data['tasks'][2]['errors']
    assert data['timing']['session_resource_seconds'] is None
    assert data['timing']['command_resource_seconds'] is None
    assert data['timing']['known_command_resource_seconds'] == 0
    assert data['timing']['complete'] is False


@pytest.mark.parametrize('kind', ['command', 'session'])
def test_conflicting_historical_snapshots_are_unknown_not_first_wins(tmp_path, kind):
    directory = tmp_path/'docs/todos/01-demo'
    one = attempt(); two = copy.deepcopy(one)
    if kind == 'command': two['commands'][0]['raw_exit_code'] = 1
    else: two['ended_at'] = stamp(25)
    card(directory, '01', [one, two])
    proc = run(tmp_path, directory)
    assert proc.returncode == 2, proc.stdout+proc.stderr
    data = json.loads(proc.stdout)
    assert any('Conflicting '+kind in error for error in data['errors'])
    assert data['timing'][kind+'_resource_seconds'] is None


@pytest.mark.parametrize('case', ['reversed', 'no-zone', 'bad-event', 'not-list'])
def test_malformed_attempt_is_reported_without_losing_other_tasks(tmp_path, case):
    directory = tmp_path/'docs/todos/01-demo'
    bad = attempt()
    if case == 'reversed': bad.update(started_at=stamp(30))
    if case == 'no-zone': bad['started_at'] = '2026-11-12T00:00:00'
    if case == 'bad-event': bad = 'broken'
    if case == 'not-list': bad['commands'] = 'bad'
    card(directory, '01', [bad]); card(directory, '02', [attempt('good')])
    proc = run(tmp_path, directory)
    assert proc.returncode == 2, proc.stdout+proc.stderr
    data = json.loads(proc.stdout)
    assert data['task_count'] == 2 and data['tasks'][1]['attempt_count'] == 1
    assert data['errors'] and data['timing']['complete'] is False


def test_empty_inventory_is_unknown_and_outside_target_rejected(tmp_path):
    directory = tmp_path/'empty'; directory.mkdir()
    proc = run(tmp_path, directory)
    assert proc.returncode == 0, proc.stdout+proc.stderr
    assert json.loads(proc.stdout)['timing']['command_resource_seconds'] is None
    outside = subprocess.run([sys.executable, '-B', str(SCRIPT), '--execution-report', str(tmp_path.parent)],
                             cwd=tmp_path, capture_output=True, encoding='utf-8')
    assert outside.returncode != 0


def test_not_started_receipt_is_unknown_duration_not_invalid_history(tmp_path):
    directory = tmp_path/'docs/todos/01-demo'
    data = attempt()
    data['commands'][0].update(status='NOT_STARTED', raw_exit_code=None, started_at=None)
    card(directory, '01', [data])
    proc = run(tmp_path, directory)
    assert proc.returncode == 0, proc.stdout+proc.stderr
    result = json.loads(proc.stdout)
    assert result['timing']['command_resource_seconds'] is None
    assert not result['errors']


def test_unrecorded_legacy_card_makes_whole_inventory_incomplete(tmp_path):
    directory = tmp_path/'docs/todos/01-demo'
    card(directory, '01', [attempt()]); card(directory, '02', [])
    proc = run(tmp_path, directory)
    assert proc.returncode == 0, proc.stdout+proc.stderr
    timing = json.loads(proc.stdout)['timing']
    assert timing['command_resource_seconds'] is None
    assert timing['known_command_resource_seconds'] == 10


@pytest.mark.parametrize('name', ['01-external.md', 'external.md'])
def test_external_task_symlink_is_inventory_error_without_reading_content(tmp_path, name, monkeypatch):
    root = tmp_path/'project'; directory = root/'docs/todos/01-demo'
    directory.mkdir(parents=True)
    external = card(tmp_path/'outside', 'PRIVATE-CARD-MARKER', [attempt()])
    (directory/name).symlink_to(external)
    proc = run(root, directory)
    assert proc.returncode == 2, proc.stdout+proc.stderr
    result = json.loads(proc.stdout)
    assert result['task_count'] == 1 and result['tasks'][0]['errors']
    assert 'PRIVATE-CARD-MARKER' not in proc.stdout
    assert result['attempt_count'] == 0
    # This also detects an early external read during nonnumeric card discovery.
    import iter_execution
    original = Path.read_text
    def bounded_read(path, *args, **kwargs):
        assert path.resolve().is_relative_to(root.resolve()), 'External content read during discovery/report'
        return original(path, *args, **kwargs)
    monkeypatch.setattr(Path, 'read_text', bounded_read)
    assert iter_execution.execution_report(directory, root)['errors']
