"""Synthetic cross-module contracts; never native delegation/approval evidence."""
import json

import pytest

from test_execution_readiness import fixture, cli, inventory, report, save
from test_filesystem_delivery_controller import fixture as frozen_fixture
from test_worktree_concurrency import git_repo_with_worktrees
from iter_sync import audit_task_file, render_task_envelope, generate_board_data


def dispatch(root, card, context, owner='lead'):
    return cli(root, '--dispatch-check', card, '--context', context.name,
               '--phase', 'implementation', '--owner', owner)


def claim(root, card):
    proc = cli(root, '--autonomy', 'claim', card, '--event-id', 'claim', '--owner', 'lead')
    assert proc.returncode == 0, proc.stdout + proc.stderr


@pytest.mark.parametrize('fault', ['authority', 'foreign-writer', 'context', 'candidate', 'phase', 'dependency'])
def test_inventory_dispatch_and_handoff_keep_distinct_gates(tmp_path, fault):
    card, context, data = fixture(tmp_path)
    claim(tmp_path, card)
    task = data['tasks']['01']
    if fault == 'authority':
        task['observations'].pop('authority')
    elif fault == 'candidate':
        task['candidate'] = 'not-the-current-candidate'
    elif fault == 'phase':
        task['phase'] = 'review'
    elif fault == 'dependency':
        dependency = card.with_name('02-unapproved.md')
        dependency.write_text('---\ntask_id: "02"\nstatus: DONE\n---\n', encoding='utf-8')
        task['dependencies'] = [dependency.relative_to(tmp_path).as_posix()]
    save(context, data)
    before = inventory(tmp_path)
    args = [] if fault == 'context' else ['--context', context.name]
    observed = cli(tmp_path, '--inventory', card.parent, '--mode', 'continue', *args)
    checked = cli(tmp_path, '--dispatch-check', card, '--phase', 'implementation',
                  '--owner', 'foreign' if fault == 'foreign-writer' else 'lead', *args)
    assert checked.returncode in (2, 3), checked.stdout + checked.stderr
    assert json.loads(checked.stdout)['readiness'] != 'READY'
    if fault == 'foreign-writer':
        assert observed.returncode == 0  # Inventory is not a writer grant.
    else:
        assert observed.returncode in (2, 3)
    handoff = render_task_envelope(card, tmp_path)['TASK_HANDOFF']
    assert handoff['acceptance_verdict'] == 'UNKNOWN'
    assert inventory(tmp_path) == before


def test_attempt_release_reclaim_preserves_progress_not_approval(tmp_path):
    card, context, _ = fixture(tmp_path)
    claim(tmp_path, card)
    assert dispatch(tmp_path, card, context).returncode == 0
    source, data = report(tmp_path, progress=[dict(kind='green', evidence='observation.txt', summary='synthetic GREEN')])
    args = ['--autonomy', 'attempt', card, '--event-id', 'attempt-a', '--owner', 'lead',
            '--executor-state', 'completed', '--evidence', source.name]
    assert cli(tmp_path, *args).returncode == 0
    before = inventory(tmp_path)
    replay = cli(tmp_path, *args)
    assert replay.returncode == 0 and json.loads(replay.stdout)['replayed']
    assert inventory(tmp_path) == before
    data['remaining_work'] = ['changed payload']; save(source, data)
    before = card.read_bytes()
    assert cli(tmp_path, *args).returncode != 0
    assert card.read_bytes() == before
    released = cli(tmp_path, '--autonomy', 'release', card, '--event-id', 'release-a',
                   '--owner', 'lead', '--executor-state', 'completed', '--evidence', 'observation.txt')
    assert released.returncode == 0, released.stdout + released.stderr
    assert dispatch(tmp_path, card, context).returncode != 0
    assert cli(tmp_path, '--autonomy', 'claim', card, '--event-id', 'claim-b', '--owner', 'next-session').returncode == 0
    handoff = render_task_envelope(card, tmp_path)['TASK_HANDOFF']
    assert handoff['execution']['attempt_count'] == 1
    assert handoff['execution']['checkpoint']['candidate'] == 'candidate-1'
    assert handoff['execution']['remaining_work'] == ['review']
    assert handoff['acceptance_verdict'] == 'UNKNOWN'


def test_two_recorded_empty_attempts_block_third_across_cli_and_inventory(tmp_path):
    card, context, _ = fixture(tmp_path)
    claim(tmp_path, card)
    source, _ = report(tmp_path)
    for number in range(2):
        proc = cli(tmp_path, '--autonomy', 'attempt', card, '--event-id', f'empty-{number}',
                   '--owner', 'lead', '--executor-state', 'completed', '--evidence', source.name)
        assert proc.returncode == 0, proc.stdout + proc.stderr
    before = inventory(tmp_path)
    checked = dispatch(tmp_path, card, context)
    scanned = cli(tmp_path, '--inventory', card.parent, '--mode', 'continue', '--context', context.name)
    assert checked.returncode == scanned.returncode == 3
    assert json.loads(checked.stdout)['execution']['no_progress_streak'] == 2
    task = json.loads(scanned.stdout)['tasks'][0]
    assert task['execution']['no_progress_streak'] == 2
    assert any('identical redispatch prohibited' in finding for finding in task['findings'])
    assert inventory(tmp_path) == before


@pytest.mark.parametrize('fault', ['bad-number', 'unknown-done'])
def test_bad_cards_remain_visible_and_never_pass(tmp_path, fault):
    card, context, _ = fixture(tmp_path)
    bad = card.with_name('02-bad.md')
    text = '---\ntask_id: "02"\nstatus: DONE\n'
    if fault == 'bad-number':
        text += 'fix_rounds: not-a-number\n'
    bad.write_text(text + '---\n', encoding='utf-8')
    before = inventory(tmp_path)
    proc = cli(tmp_path, '--inventory', card.parent, '--mode', 'takeover', '--context', context.name)
    assert proc.returncode == 3
    tasks = json.loads(proc.stdout)['tasks']
    assert len(tasks) == 2 and tasks[0]['readiness'] == 'READY'
    assert tasks[1]['readiness'] != 'READY' and tasks[1]['acceptance_verdict'] != 'PASS'
    assert inventory(tmp_path) == before


@pytest.mark.parametrize('target', ['source', 'evidence', 'body'])
def test_frozen_fs_drift_reaches_audit_envelope_and_board(tmp_path, target):
    card, _, _ = frozen_fixture(tmp_path)
    assert audit_task_file(card)['verdict'] == 'PASS'
    path = {'source': tmp_path/'src/a.py', 'evidence': tmp_path/'evidence/green.txt', 'body': card}[target]
    path.write_text(path.read_text(encoding='utf-8') + '\nchanged after review\n', encoding='utf-8')
    before = inventory(tmp_path)
    assert audit_task_file(card)['verdict'] != 'PASS'
    assert render_task_envelope(card, tmp_path)['TASK_HANDOFF']['acceptance_verdict'] != 'PASS'
    board = generate_board_data(card.parent)
    assert len(board['cards']) == 1
    assert board['cards'][0]['acceptance_verdict'] != 'PASS'
    assert board['accepted'] == 0 and board['conclusion'] != 'PASS'
    assert inventory(tmp_path) == before


def test_feature_branch_root_sync_refusal_is_byte_preserving(git_repo_with_worktrees):
    _, worktree, _ = git_repo_with_worktrees
    root_index = worktree/'docs/todos/README.md'
    before = root_index.read_bytes()
    proc = cli(worktree, worktree)
    assert proc.returncode != 0 and 'Zero-Root-Touch' in proc.stdout + proc.stderr
    assert root_index.read_bytes() == before
