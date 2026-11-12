import subprocess
import json
import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from iter_sync import audit_task_file, check_branch_isolation
from test_worktree_concurrency import git_repo_with_worktrees, run_cmd

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/iter_sync.py"


def make_reviewed_candidate(wt, kind="Strict-TDD"):
    """Synthetic receipt fixture: tests structure/version gates, not real task acceptance."""
    base = run_cmd(["git", "rev-parse", "HEAD"], wt).stdout.strip()
    card = wt / "docs/todos/01-iter-one/01-task.md"
    evidence = wt / "docs/todos/01-iter-one/evidence/01"
    evidence.mkdir(parents=True)
    names = {"Strict-TDD": ["red", "green", "regression"],
             "UI-Component": ["interaction", "states", "visual", "regression"],
             "Refactor-Benchmark": ["baseline", "regression", "compatibility", "benchmark_before", "benchmark_after"],
             "Spike-Discovery": ["experiment", "decision", "interfaces"]}[kind]
    observations = {"states", "visual", "compatibility", "decision", "interfaces"}
    checks = []
    for name in names:
        output = evidence / (name + ".txt")
        output.write_text("synthetic fixture: " + name, encoding="utf-8")
        check = {"name": name, "kind": "observation" if name in observations else "command",
                 "summary": "synthetic fixture observed result", "output": output.relative_to(wt).as_posix()}
        if name not in observations:
            check.update(command="python -m pytest tests/test_behavior.py", cwd=".", exit_code=1 if name == "red" else 0)
        if name == "red":
            check["failure_kind"] = "assertion"
        checks.append(check)
    report = evidence / "review.txt"
    report.write_text("synthetic independent review fixture", encoding="utf-8")
    readme = card.parent / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + '\n<!-- iter:goal -->\nFrozen iteration goal.\n<!-- /iter:goal -->\n', encoding="utf-8")
    card.write_text(f'---\nschema_version: 1\ntask_id: "01"\ntype: {kind}\nstatus: TESTING\n'
                    f'base_sha: {base}\nhead_sha: ""\nreview_status: PENDING\n'
                    f'tdd_verified: {"true" if kind == "Strict-TDD" else "false"}\n'
                    'review_receipt: docs/todos/01-iter-one/evidence/01/review.json\n---\n'
                    '## 1. Objective\nKeep behavior stable.\n'
                    '<!-- iter:scope -->\n| File path | Role |\n| --- | --- |\n'
                    '| `src/a.py` | implementation |\n'
                    '| `docs/todos/01-iter-one/evidence/01/` | evidence |\n<!-- /iter:scope -->\n'
                    '<!-- iter:acceptance -->\n- [x] Observable behavior\n<!-- /iter:acceptance -->\n'
                    '<!-- iter:ledger -->\nPending report\n<!-- /iter:ledger -->\n', encoding="utf-8")
    (wt / "src").mkdir(exist_ok=True)
    (wt / "src/a.py").write_text("value = 1\n", encoding="utf-8")
    run_cmd(["git", "add", "."], wt)
    run_cmd(["git", "commit", "-m", "implement reviewed task"], wt)
    head = run_cmd(["git", "rev-parse", "HEAD"], wt).stdout.strip()
    receipt = {"schema_version": 1, "task_id": "01", "type": kind,
               "task_path": card.relative_to(wt).as_posix(), "base_sha": base,
               "head_sha": head, "contract_sha": head, "implementer": "implementer-session",
               "reviewer": "independent-review-session", "verdict": "APPROVED",
               "review_report": report.relative_to(wt).as_posix(), "checks": checks}
    receipt_path = evidence / "review.json"
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    text = card.read_text(encoding="utf-8").replace("status: TESTING", "status: DONE").replace('head_sha: ""', f"head_sha: {head}").replace("review_status: PENDING", "review_status: APPROVED")
    card.write_text(text, encoding="utf-8")
    run_cmd(["git", "add", "."], wt)
    run_cmd(["git", "commit", "-m", "record approval and evidence"], wt)
    return card, receipt_path, receipt


def test_declared_done_without_evidence_is_unknown(tmp_path):
    card = tmp_path / "01-task.md"
    for flags in ("", "tdd_verified: true\nreview_status: APPROVED\n"):
        card.write_text("---\nstatus: DONE\n" + flags + "---\n", encoding="utf-8")
        result = audit_task_file(card)
        assert result["status"] == "DONE"
        assert result["is_valid_done"] is False
        assert result.get("verdict") == "UNKNOWN"


def test_strict_cli_checks_committed_done_cards(git_repo_with_worktrees):
    _, wt, _ = git_repo_with_worktrees
    card = wt / "docs/todos/01-iter-one/01-task.md"
    original = "---\nstatus: DONE\ntdd_verified: true\nreview_status: APPROVED\n---\n"
    card.write_text(original, encoding="utf-8")
    run_cmd(["git", "add", str(card)], wt)
    run_cmd(["git", "commit", "-m", "declare legacy DONE"], wt)
    result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--check-branch", "--strict", str(wt)],
                            capture_output=True, encoding="utf-8")
    assert result.returncode == 2, result.stdout + result.stderr
    assert "UNKNOWN" in result.stderr
    assert card.read_text(encoding="utf-8") == original


def test_spike_acceptance_does_not_require_fake_tdd(git_repo_with_worktrees):
    _, wt, _ = git_repo_with_worktrees
    card, _, _ = make_reviewed_candidate(wt, "Spike-Discovery")
    result = audit_task_file(card)
    assert result["is_valid_done"] is True, result
    assert result.get("verdict") == "PASS"


def test_receipt_rejects_environment_red_and_self_review(git_repo_with_worktrees):
    _, wt, _ = git_repo_with_worktrees
    card, path, receipt = make_reviewed_candidate(wt)
    receipt["reviewer"] = receipt["implementer"]
    receipt["checks"][0]["failure_kind"] = "environment"
    path.write_text(json.dumps(receipt), encoding="utf-8")
    result = audit_task_file(card)
    assert result["is_valid_done"] is False
    assert any("independent" in v.lower() or "assertion" in v.lower() for v in result["violations"])


@pytest.mark.parametrize("kind", ["Strict-TDD", "UI-Component", "Refactor-Benchmark", "Spike-Discovery"])
def test_all_types_accept_bookkeeping_and_strict_cli(git_repo_with_worktrees, kind):
    _, wt, _ = git_repo_with_worktrees
    card, _, _ = make_reviewed_candidate(wt, kind)
    text = card.read_text(encoding="utf-8").replace("Pending report", "Approval registered")
    card.write_text(text, encoding="utf-8")
    run_cmd(["git", "add", "."], wt)
    run_cmd(["git", "commit", "-m", "bookkeeping only"], wt)
    assert audit_task_file(card)["is_valid_done"] is True
    result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--check-branch", "--strict", str(wt)], capture_output=True, encoding="utf-8")
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("target,old,new", [
    ("src/a.py", "value = 1", "value = 2"),
    ("docs/todos/01-iter-one/01-task.md", "Keep behavior stable.", "Change the objective."),
    ("docs/todos/01-iter-one/01-task.md", "Observable behavior", "Weaker criterion"),
    ("docs/todos/01-iter-one/README.md", "Frozen iteration goal.", "Changed global goal."),
    ("docs/todos/01-iter-one/evidence/01/green.txt", "synthetic", "replaced"),
])
def test_reviewed_scope_and_contract_drift_rejected(git_repo_with_worktrees, target, old, new):
    _, wt, _ = git_repo_with_worktrees
    card, _, _ = make_reviewed_candidate(wt)
    path = wt / target
    path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
    run_cmd(["git", "add", "."], wt)
    run_cmd(["git", "commit", "-m", "unreviewed drift"], wt)
    result = audit_task_file(card)
    assert result["is_valid_done"] is False, result


def test_unrelated_change_preserves_receipt_but_branch_requires_coverage(git_repo_with_worktrees):
    _, wt, _ = git_repo_with_worktrees
    card, _, _ = make_reviewed_candidate(wt)
    (wt / "uncovered.py").write_text("value = 2\n", encoding="utf-8")
    run_cmd(["git", "add", "."], wt)
    run_cmd(["git", "commit", "-m", "uncovered unrelated work"], wt)
    assert audit_task_file(card)["is_valid_done"] is True
    result = check_branch_isolation(wt, strict=True)
    assert result["passed"] is False, result
    assert any("uncovered.py" in v for v in result["violations"])


@pytest.mark.parametrize("mutation", ["missing_output", "type", "base", "bad_head", "bool_exit", "missing_check", "scope"])
def test_invalid_receipt_rejected(git_repo_with_worktrees, mutation):
    _, wt, _ = git_repo_with_worktrees
    card, path, receipt = make_reviewed_candidate(wt)
    if mutation == "missing_output":
        (wt / receipt["checks"][1]["output"]).unlink()
    elif mutation == "type":
        receipt["type"] = "Spike-Discovery"
    elif mutation == "base":
        receipt["base_sha"] = receipt["head_sha"]
    elif mutation == "bad_head":
        old = receipt["head_sha"]
        receipt["head_sha"] = "f" * 40
        card.write_text(card.read_text(encoding="utf-8").replace(old, "f" * 40), encoding="utf-8")
    elif mutation == "bool_exit":
        receipt["checks"][1]["exit_code"] = False
    elif mutation == "missing_check":
        receipt["checks"] = receipt["checks"][:-1]
    elif mutation == "scope":
        card.write_text(card.read_text(encoding="utf-8").replace("`src/a.py`", "`src/`"), encoding="utf-8")
    path.write_text(json.dumps(receipt), encoding="utf-8")
    assert audit_task_file(card)["is_valid_done"] is False
