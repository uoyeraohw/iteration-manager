"""Synthetic benchmark fixtures must exercise real acceptance bindings."""
import importlib.util
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location('approval_chain', Path(__file__).parent / 'benchmarks/approval_chain.py')
bench = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)

@pytest.mark.parametrize('mode', ['git', 'filesystem'])
def test_approved_fixture_and_independent_binding_drift(tmp_path, mode):
    root = tmp_path / 'project'
    directory, cards, context = bench.make_workload(root, mode, 2)
    assert [bench.audit_task_file(card)['verdict'] for card in cards] == ['PASS', 'PASS']
    assert bench.generate_board_data(directory)['accepted'] == 2
    source = root / 'src/001.py'
    source.write_text('drifted source\n', encoding='utf-8')
    if mode == 'git':
        bench.run_git(root, 'add', '.')
        bench.run_git(root, 'commit', '-m', 'Synthetic unreviewed drift')
    result = bench.audit_task_file(cards[0])
    assert result['verdict'] != 'PASS', result
    assert bench.audit_task_file(cards[1])['verdict'] == 'PASS'

@pytest.mark.parametrize('mode', ['git', 'filesystem'])
def test_measurement_exercises_four_real_paths(tmp_path, mode):
    root = tmp_path / 'project'
    directory, cards, context = bench.make_workload(root, mode, 2)
    results = bench.benchmark(root, directory, cards, context, 1, lambda _: None)
    assert set(results) == {'board', 'all_envelopes', 'inventory', 'http_evidence'}
    assert all(row['trials'][0]['path_read_bytes'] > 0 for row in results.values())
    assert results['http_evidence']['trials'][0]['path_read_calls'] > 0
    if mode == 'git':
        assert all(row['trials'][0]['git_calls'] > 0 for row in results.values())
    else:
        assert results['board']['trials'][0]['git_calls'] == 0
