"""New fields are tested through the callable legacy entry before extraction."""
import json
import inspect
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from iter_autonomy import load_state
from iter_sync import generate_board_data, render_task_envelope


@pytest.mark.parametrize('mode', ['git', 'filesystem'])
@pytest.mark.parametrize('has_checkpoint', [False, True])
def test_legacy_board_exposes_same_handoff_fields(tmp_path, mode, has_checkpoint):
    directory = tmp_path / 'docs/todos/03-contract'
    directory.mkdir(parents=True)
    metadata = dict(schema_version='1', task_id='03', status='IN_PROGRESS', type='Strict-TDD')
    if mode == 'filesystem':
        (directory / 'iteration-delivery.json').write_text(
            json.dumps(dict(schema_version=1, mode=mode)), encoding='utf-8')
        metadata.update(delivery_mode=mode, candidate_id='fs-candidate-a')
    state = load_state(metadata)
    if has_checkpoint:
        state['events']['attempt-a'] = {'input': {'action': 'attempt', 'attempt': {
            'candidate': 'fixed-candidate', 'phase': 'implementation',
            'checkpoint': 'valid old-entry RED', 'remaining_work': ['extract query layer'],
            'progress': [{'kind': 'red', 'evidence': 'red.txt', 'summary': 'assertion failure'}],
            'source': 'attempt.json',
        }}}
    metadata['autonomy_state'] = json.dumps(state)
    card = directory / '03-task.md'
    card.write_text('---\n' + ''.join(f'{key}: {json.dumps(value)}\n' for key, value in metadata.items())
                    + '---\n', encoding='utf-8')
    before = {path: path.read_bytes() for path in directory.iterdir()}
    handoff = render_task_envelope(card, tmp_path)['TASK_HANDOFF']
    board_card = generate_board_data(directory)['cards'][0]
    required = {'delivery_mode', 'candidate_id', 'execution'}
    assert required <= board_card.keys(), f'legacy board missing handoff fields: {required - board_card.keys()}'
    assert {key: board_card[key] for key in required} == {key: handoff[key] for key in required}
    assert board_card['delivery_mode'] == mode
    if mode == 'filesystem':
        assert board_card['candidate_id'] == 'fs-candidate-a'
    execution = board_card['execution']
    if has_checkpoint:
        assert execution['checkpoint']['summary'] == 'valid old-entry RED'
        assert execution['remaining_work'] == ['extract query layer']
    else:
        assert execution['checkpoint'] is None
    assert {path: path.read_bytes() for path in directory.iterdir()} == before


def test_query_exports_keep_legacy_signatures():
    import iter_queries as query
    import iter_sync as legacy
    for name in ('discover_task_files', 'audit_task_file', 'render_task_envelope'):
        assert getattr(legacy, name) is getattr(query, name)
    assert str(inspect.signature(query.discover_task_files)) == '(directory: pathlib.Path, read_root: pathlib.Path | None = None) -> list[pathlib.Path]'


def test_query_and_consumers_do_not_load_sync_or_cli(tmp_path):
    scripts = Path(__file__).resolve().parents[1] / 'scripts'
    code = (f'import sys; sys.path.insert(0, {str(scripts)!r}); '
            'import iter_queries, iter_inventory, iter_preflight, iter_execution; '
            'assert "iter_sync" not in sys.modules; assert "iter_cli" not in sys.modules; '
            f'iter_inventory.inventory(__import__("pathlib").Path({str(tmp_path)!r}), '
            f'__import__("pathlib").Path({str(tmp_path)!r}), "continue"); '
            'assert "iter_sync" not in sys.modules')
    result = subprocess.run([sys.executable, '-B', '-c', code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_inventory_query_audit_reused_only_within_call(tmp_path, monkeypatch):
    import iter_queries as query
    from iter_inventory import inventory
    from test_execution_readiness import fixture
    card, ctx, data = fixture(tmp_path)
    second = card.with_name('02-task.md')
    second.write_text(card.read_text(encoding='utf-8').replace('task_id: "01"', 'task_id: "02"'), encoding='utf-8')
    data['tasks']['02'] = json.loads(json.dumps(data['tasks']['01']))
    data['tasks']['02']['dependencies'] = [card.relative_to(tmp_path).as_posix()]
    ctx.write_text(json.dumps(data), encoding='utf-8')
    calls = []
    original = query.audit_task_file
    def observed(path):
        calls.append(path.name)
        return original(path)
    monkeypatch.setattr(query, 'audit_task_file', observed)
    for expected in (1, 2):
        report = inventory(card.parent, tmp_path, 'continue', ctx.name)
        assert report['readiness'] == 'BLOCKED'
        assert calls.count(card.name) == calls.count(second.name) == expected


def test_query_observes_changes_and_rejects_bad_profile(tmp_path):
    import iter_queries as query
    directory = tmp_path / 'docs/todos/03-contract'
    directory.mkdir(parents=True)
    card = directory / '03-task.md'
    card.write_text('---\nstatus: TODO\n---\n', encoding='utf-8')
    assert query.audit_task_file(card)['status'] == 'TODO'
    card.write_text('---\nstatus: invalid\n---\n', encoding='utf-8')
    assert query.audit_task_file(card)['status'] == 'UNKNOWN'
    assert query.render_task_envelope(card, tmp_path)['TASK_HANDOFF']['status'] == 'UNKNOWN'
    (directory / 'iteration-delivery.json').write_text('{}', encoding='utf-8')
    assert query.audit_task_file(card)['verdict'] == 'FAIL'
    assert 'error' in query.render_task_envelope(card, tmp_path)
    board = generate_board_data(directory)['cards'][0]
    assert board['sources'] == [] and board['delivery_mode'] == 'UNKNOWN'
    assert board['candidate_id'] is None and board['execution'] is None
