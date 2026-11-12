"""Synthetic filesystem fixtures; not AIMovie completion evidence."""
import copy
import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from iter_sync import audit_task_file, sync_local_iteration, generate_board_data

NAMES = {
    "Strict-TDD": ("red", "green", "regression"),
    "UI-Component": ("interaction", "states", "visual", "regression"),
    "Refactor-Benchmark": ("baseline", "regression", "compatibility", "benchmark_before", "benchmark_after"),
    "Spike-Discovery": ("experiment", "decision", "interfaces"),
}
OBS = {"states", "visual", "compatibility", "decision", "interfaces"}

def dump(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")

def fixture(root, kind="Strict-TDD", tool=False):
    it = root / "docs/todos/01-synthetic"
    it.mkdir(parents=True)
    (root / "src").mkdir()
    (root / "evidence").mkdir()
    (root / "frozen").mkdir()
    (root / "src/a.py").write_bytes(b"value = 1\n")
    dump(it / "iteration-delivery.json", {"schema_version": 1, "mode": "filesystem"})
    (it / "README.md").write_text("# Synthetic\n<!-- iter:goal -->\nFrozen goal\n<!-- /iter:goal -->\n", encoding="utf-8")
    card = it / "01-task.md"
    rel = card.relative_to(root).as_posix()
    content = ("---\nschema_version: 1\ntask_id: \"01\"\ntype: " + kind
      + "\nstatus: DONE\ndelivery_mode: filesystem\ncandidate_id: synthetic-current-1\n"
      + "review_status: APPROVED\ntdd_verified: true\nreview_receipt: evidence/review.json\n---\n"
      + "## Objective\nSynthetic observable behavior\n"
      + "<!-- iter:scope -->\n| File path | Role |\n| --- | --- |\n"
      + "| `src/a.py` | implementation |\n| `evidence/` | raw evidence |\n<!-- /iter:scope -->\n"
      + "<!-- iter:acceptance -->\n- [x] Synthetic acceptance\n<!-- /iter:acceptance -->\n"
      + "<!-- iter:ledger -->\nSynthetic ledger\n<!-- /iter:ledger -->\n")
    card.write_text(content, encoding="utf-8")
    (root / "frozen/contract.md").write_bytes(card.read_bytes())
    (root / "frozen/goal.md").write_bytes((it / "README.md").read_bytes())
    checks = []
    for name in NAMES[kind]:
        (root / ("evidence/" + name + ".txt")).write_text("synthetic " + name, encoding="utf-8")
        obs = name in OBS or (tool and kind == "UI-Component" and name == "interaction")
        item = dict(name=name, kind="observation" if obs else "command",
                    summary="Synthetic assertion/observation", output="evidence/" + name + ".txt")
        if not obs:
            item.update(command="python -m pytest synthetic.py", cwd=".", exit_code=1 if name == "red" else 0)
        if name == "red":
            item["failure_kind"] = "assertion"
        if tool and name == "interaction":
            item.update(source_tool="synthetic-native-ui", observed_at="2026-11-12T03:00:00+00:00")
        checks.append(item)
    (root / "evidence/review.txt").write_text("Synthetic independent review fixture", encoding="utf-8")
    receipt = dict(schema_version=1, receipt_kind="current-filesystem-review-v1",
      delivery_mode="filesystem", task_id="01", type=kind, task_path=rel,
      candidate_id="synthetic-current-1", recorded_at="2026-11-12T03:00:00+00:00",
      implementer="synthetic-author", reviewer="synthetic-reviewer",
      verdict="APPROVED", review_report="evidence/review.txt", checks=checks,
      candidate_manifest="frozen/manifest.json", contract_snapshot="frozen/contract.md",
      goal_snapshot="frozen/goal.md")
    files = []
    for index, source in enumerate(["src/a.py"] + [c["output"] for c in checks]):
        snap = "frozen/file-" + str(index)
        (root / snap).write_bytes((root / source).read_bytes())
        files.append(dict(path=source, snapshot=snap))
    manifest = dict(candidate_id=receipt["candidate_id"], files=files)
    dump(root / "frozen/manifest.json", manifest)
    dump(root / "evidence/review.json", receipt)
    return card, receipt, manifest

@pytest.mark.parametrize("kind", list(NAMES))
def test_filesystem_valid_current_candidate_passes_without_git(tmp_path, kind):
    card, _, _ = fixture(tmp_path, kind)
    audit = audit_task_file(card)
    assert audit["verdict"] == "PASS", audit
    result = sync_local_iteration(card.parent, dry_run=True, strict=True)
    assert not result["gate_violations"], result

def test_native_ui_observation_is_explicit(tmp_path):
    card, r, _ = fixture(tmp_path, "UI-Component", tool=True)
    assert audit_task_file(card)["verdict"] == "PASS"
    del r["checks"][0]["source_tool"]
    dump(tmp_path / "evidence/review.json", r)
    assert audit_task_file(card)["verdict"] != "PASS"

@pytest.mark.parametrize("mutation", [
  "missing_output", "self_review", "environment_red", "bool_exit", "wrong_kind",
  "invalid_profile", "no_profile", "escape", "alias", "self_snapshot", "cross_snapshot",
  "source_drift", "evidence_drift", "contract_drift", "goal_drift", "new_directory_file",
  "sha", "wrong_candidate", "missing_manifest_entry", "extra_manifest_source",
  "own_contract", "own_goal", "missing_goal", "naive_recorded", "wrong_receipt_kind",
  "missing_required", "duplicate_check", "bool_schema", "metadata_sha", "manifest_candidate",
])
def test_filesystem_rejects_invalid_binding_or_receipt(tmp_path, mutation):
    card, r, m = fixture(tmp_path)
    if mutation == "missing_output":
        (tmp_path / "evidence/green.txt").unlink()
    elif mutation == "self_review": r["reviewer"] = r["implementer"]
    elif mutation == "environment_red": r["checks"][0]["failure_kind"] = "environment"
    elif mutation == "bool_exit": r["checks"][1]["exit_code"] = False
    elif mutation == "wrong_kind": r["checks"][1]["kind"] = "observation"
    elif mutation == "invalid_profile": dump(card.parent / "iteration-delivery.json", {"schema_version": 1, "mode": "typo"})
    elif mutation == "no_profile": (card.parent / "iteration-delivery.json").unlink()
    elif mutation == "escape": m["files"][0]["snapshot"] = "../outside.py"
    elif mutation == "alias":
        duplicate = copy.deepcopy(m["files"][0]); duplicate["path"] = "src/./a.py"; m["files"].append(duplicate)
    elif mutation == "self_snapshot": m["files"][0]["snapshot"] = m["files"][0]["path"]
    elif mutation == "cross_snapshot":
        m["files"][0]["snapshot"] = m["files"][1]["path"]
    elif mutation == "source_drift": (tmp_path / "src/a.py").write_text("value=2", encoding="utf-8")
    elif mutation == "evidence_drift": (tmp_path / "evidence/green.txt").write_text("altered", encoding="utf-8")
    elif mutation == "contract_drift": card.write_text(card.read_text(encoding="utf-8").replace("Synthetic observable behavior", "Changed criterion"), encoding="utf-8")
    elif mutation == "goal_drift": (card.parent / "README.md").write_text("<!-- iter:goal -->Changed<!-- /iter:goal -->", encoding="utf-8")
    elif mutation == "new_directory_file": (tmp_path / "evidence/new.txt").write_text("unbound", encoding="utf-8")
    elif mutation == "sha": r["head_sha"] = "f" * 40
    elif mutation == "wrong_candidate": r["candidate_id"] = "another"
    elif mutation == "missing_manifest_entry": m["files"].pop()
    elif mutation == "extra_manifest_source":
        (tmp_path / "other.txt").write_text("outside scope", encoding="utf-8")
        (tmp_path / "frozen/extra").write_text("outside scope", encoding="utf-8")
        m["files"].append(dict(path="other.txt", snapshot="frozen/extra"))
    elif mutation == "own_contract": r["contract_snapshot"] = card.relative_to(tmp_path).as_posix()
    elif mutation == "own_goal": r["goal_snapshot"] = (card.parent / "README.md").relative_to(tmp_path).as_posix()
    elif mutation == "missing_goal":
        (tmp_path / "frozen/goal.md").write_text("# No goal", encoding="utf-8")
        (card.parent / "README.md").write_text("# No goal", encoding="utf-8")
    elif mutation == "naive_recorded": r["recorded_at"] = "2026-11-12T03:00:00"
    elif mutation == "wrong_receipt_kind": r["receipt_kind"] = "legacy"
    elif mutation == "missing_required": r["checks"].pop()
    elif mutation == "duplicate_check": r["checks"].append(copy.deepcopy(r["checks"][0]))
    elif mutation == "bool_schema": r["schema_version"] = True
    elif mutation == "metadata_sha":
        card.write_text(card.read_text(encoding="utf-8").replace("status: DONE", "head_sha: fffff\nstatus: DONE"), encoding="utf-8")
        (tmp_path / "frozen/contract.md").write_bytes(card.read_bytes())
    elif mutation == "manifest_candidate": m["candidate_id"] = "wrong"
    dump(tmp_path / "frozen/manifest.json", m)
    dump(tmp_path / "evidence/review.json", r)
    assert audit_task_file(card)["verdict"] != "PASS", mutation

def test_invalid_profile_blocks_non_done_local_strict(tmp_path):
    card, _, _ = fixture(tmp_path)
    card.write_text(card.read_text(encoding="utf-8").replace("status: DONE", "status: TODO"), encoding="utf-8")
    dump(card.parent / "iteration-delivery.json", [])
    assert sync_local_iteration(card.parent, dry_run=True, strict=True)["gate_violations"]

@pytest.mark.parametrize("scope", ["missing/", "missing.py", "src/a.py/"])
def test_missing_or_wrong_kind_scope_is_rejected(tmp_path, scope):
    card, _, _ = fixture(tmp_path)
    text = card.read_text(encoding="utf-8").replace("| `src/a.py`", "| `" + scope + "`")
    card.write_text(text, encoding="utf-8")
    (tmp_path / "frozen/contract.md").write_text(text, encoding="utf-8")
    assert audit_task_file(card)["verdict"] == "FAIL"

def test_invalid_profile_retains_declared_state(tmp_path):
    card, _, _ = fixture(tmp_path)
    dump(card.parent / "iteration-delivery.json", {"schema_version": True, "mode": "filesystem"})
    result = audit_task_file(card)
    assert result["status"] == "DONE"
    assert result["verdict"] == "FAIL"

def test_project_root_goal_is_not_iteration_goal(tmp_path):
    card, _, _ = fixture(tmp_path)
    (tmp_path / "README.md").write_text("<!-- iter:goal -->Changed<!-- /iter:goal -->", encoding="utf-8")
    assert audit_task_file(card)["verdict"] == "PASS"

def test_snapshot_symlink_outside_project_is_rejected(tmp_path):
    card, _, m = fixture(tmp_path)
    external = tmp_path.parent / (tmp_path.name + "-outside.txt")
    external.write_bytes((tmp_path / "src/a.py").read_bytes())
    link = tmp_path / "frozen/outside-link"
    try:
        link.symlink_to(external)
    except OSError as error:
        pytest.skip("Host does not grant symlink creation: " + str(error))
    m["files"][0]["snapshot"] = "frozen/outside-link"
    dump(tmp_path / "frozen/manifest.json", m)
    assert audit_task_file(card)["verdict"] == "FAIL"


def test_filesystem_preserves_budget_fuse(tmp_path):
    card, _, _ = fixture(tmp_path)
    text = card.read_text(encoding="utf-8").replace("status: DONE", "fix_rounds: 5\nstatus: DONE")
    card.write_text(text, encoding="utf-8")
    # Execution metadata is mutable; no new historical budget event is invented.
    board = generate_board_data(card.parent)
    assert board["cards"][0]["acceptance_verdict"] == "BLOCKED"
    assert sync_local_iteration(card.parent, dry_run=True, strict=True)["gate_violations"]

@pytest.mark.parametrize("entry", ["branch", "global"])
def test_filesystem_profile_cannot_replace_git_receipts_in_other_strict_entrypoints(tmp_path, entry):
    import subprocess
    from iter_sync import check_branch_isolation, sync_todos
    card, _, _ = fixture(tmp_path)
    (tmp_path / "docs/todos/README.md").write_text("# Synthetic global index", encoding="utf-8")
    for argv in (
        ["git", "init", "-b", "main"], ["git", "config", "user.name", "Synthetic Test"],
        ["git", "config", "user.email", "synthetic@example.invalid"],
        ["git", "add", "."], ["git", "commit", "-m", "synthetic filesystem fixture"],
        ["git", "checkout", "-b", "feat/iter-01"],
    ):
        subprocess.run(argv, cwd=tmp_path, check=True, capture_output=True)
    assert audit_task_file(card)["verdict"] == "PASS"  # Authorized local filesystem candidate.
    if entry == "branch":
        result = check_branch_isolation(tmp_path, strict=True)
        assert not result["passed"], result
    else:
        result = sync_todos(tmp_path / "docs/todos", dry_run=True, strict=True)
        assert result["gate_violations"], result


