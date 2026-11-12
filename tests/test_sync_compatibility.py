import subprocess
import sys
import pytest
from test_worktree_concurrency import git_repo_with_worktrees
from pathlib import Path
from test_completion_gates import make_reviewed_candidate
from iter_sync import sync_local_iteration, STATUS_BADGE_MAP

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/iter_sync.py'


def test_strict_local_cli_fails_unknown_done_but_default_warns(git_repo_with_worktrees):
    _, wt, _ = git_repo_with_worktrees
    card = wt / 'docs/todos/01-iter-one/01-task.md'
    card.write_text('---\nstatus: DONE\n---\n', encoding='utf-8')
    for flags, expected in (([], 0), (['--strict'], 2)):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--local', *flags, str(wt)], capture_output=True, encoding='utf-8')
        assert result.returncode == expected, result.stdout + result.stderr
        assert 'UNKNOWN' in result.stderr


def test_strict_global_cli_fails_unknown_done(git_repo_with_worktrees):
    repo, _, _ = git_repo_with_worktrees
    card = repo / 'docs/todos/01-iter-one/01-task.md'
    card.write_text('---\nstatus: DONE\n---\n', encoding='utf-8')
    result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--strict', str(repo)], capture_output=True, encoding='utf-8')
    assert result.returncode == 2, result.stdout + result.stderr


def test_strict_local_rejects_uncommitted_candidate(git_repo_with_worktrees):
    _, wt, _ = git_repo_with_worktrees
    card, _, _ = make_reviewed_candidate(wt)
    (wt / 'untracked.txt').write_text('other owner work', encoding='utf-8')
    result = sync_local_iteration(card.parent, strict=True, dry_run=True)
    assert any('Uncommitted' in v for v in result['gate_violations']), result


@pytest.mark.parametrize('header', ['Task | Status | Commit', '详细卡片索引 | 状态 | Commit'])
def test_local_sync_updates_linked_legacy_status_only(git_repo_with_worktrees, header):
    repo, wt, _ = git_repo_with_worktrees
    card, _, _ = make_reviewed_candidate(wt)
    root_index = wt / 'docs/todos/README.md'
    root_before = root_index.read_bytes()
    readme = card.parent / 'README.md'
    original = readme.read_text(encoding='utf-8')
    unrelated = '| Item | Status | Commit |\n| --- | --- | --- |\n| [API](01-task.md) | HTTP 200 | manual |\n'
    old_table = (f'| {header} |\n| --- | --- | --- |\n'
                 '| [01](01-task.md) | TODO | keep-this-C |\n'
                 '| [02](02-other.md) | TODO | other-C |\n')
    readme.write_text(original + '\n' + old_table + '\n' + unrelated, encoding='utf-8')

    result = sync_local_iteration(card.parent)
    updated = readme.read_text(encoding='utf-8')
    assert result['accepted'] == 1
    assert f'| [01](01-task.md) | {STATUS_BADGE_MAP["DONE"]} / 验收:PASS | keep-this-C |' in updated
    assert '| [02](02-other.md) | TODO | other-C |' in updated
    assert unrelated in updated
    assert '声明DONE 1/1 · 验收PASS 1/1' in updated
    assert root_index.read_bytes() == root_before
