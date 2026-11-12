import json
import subprocess
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from iter_sync import audit_scope_firewall
from test_worktree_concurrency import git_repo_with_worktrees, run_cmd

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/iter_sync.py"


def test_missing_scope_is_not_an_empty_diff_pass(git_repo_with_worktrees):
    _, wt, _ = git_repo_with_worktrees
    card = wt / "docs/todos/01-iter-one/01-task.md"
    head = run_cmd(["git", "rev-parse", "HEAD"], wt).stdout.strip()
    result = audit_scope_firewall(wt, head, head, card)
    assert result["passed"] is False
    assert any("scope" in message.lower() for message in result["violations"])


@pytest.mark.parametrize("mode", ["staged", "unstaged", "untracked"])
def test_precommit_cli_detects_changes_and_never_reverts(git_repo_with_worktrees, mode, tmp_path):
    _, wt, _ = git_repo_with_worktrees
    card = wt / "docs/todos/01-iter-one/01-task.md"
    card.write_text('---\nstatus: TODO\n---\n## 5. File & Scope Impact\n'
                    '| File path | Role |\n| --- | --- |\n| `allowed.py` | code |\n', encoding="utf-8")
    outside = wt / "outside.txt"
    if mode == "unstaged":
        outside.write_text("original", encoding="utf-8")
        run_cmd(["git", "add", "outside.txt"], wt)
        run_cmd(["git", "commit", "-m", "other owner baseline"], wt)
    head = run_cmd(["git", "rev-parse", "HEAD"], wt).stdout.strip()
    outside.write_text("other owner's work stays", encoding="utf-8")
    if mode == "staged":
        run_cmd(["git", "add", "outside.txt"], wt)
    baseline = tmp_path / "dirty.json"
    baseline.write_text(json.dumps(["outside.txt"]), encoding="utf-8")
    result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--check-scope", head, head,
                             str(card), str(wt), "--include-worktree", "--baseline-dirty", str(baseline)],
                            capture_output=True, encoding="utf-8")
    assert result.returncode == 2, result.stdout + result.stderr
    assert "outside.txt" in result.stderr
    assert outside.read_text(encoding="utf-8") == "other owner's work stays"
