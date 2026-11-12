import json
import pytest
from pathlib import Path
from iter_sync import audit_task_file

def create_synthetic_fs_fixture(tmp_path: Path):
    root = tmp_path
    iter_dir = root / "docs" / "todos" / "01-test-iter"
    iter_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. iteration-delivery.json
    delivery_cfg = iter_dir / "iteration-delivery.json"
    delivery_cfg.write_text(json.dumps({
        "schema_version": 1,
        "mode": "filesystem"
    }), encoding="utf-8")
    
    # 2. README.md with goal
    readme_content = """# Iteration 01
<!-- iter:goal -->
迭代核心目标与全局约束：验证纯文件系统交付收据能力。
<!-- /iter:goal -->
"""
    (iter_dir / "README.md").write_text(readme_content, encoding="utf-8")
    
    # 3. snapshots & evidence outside scope
    snapshots_dir = root / "artifacts" / "snapshots"
    evidence_dir = root / "artifacts" / "evidence"
    snapshots_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    goal_snap = snapshots_dir / "goal_snap.md"
    goal_snap.write_text(readme_content, encoding="utf-8")
    
    check_red = evidence_dir / "red.txt"
    check_red.write_text("AssertionError: red failed", encoding="utf-8")
    check_green = evidence_dir / "green.txt"
    check_green.write_text("PASSED", encoding="utf-8")
    check_regression = evidence_dir / "regression.txt"
    check_regression.write_text("PASSED", encoding="utf-8")
    
    report_file = root / "artifacts" / "review_report.md"
    report_file.write_text("LGTM approved", encoding="utf-8")
    
    # 4. scoped file
    src_file = root / "src" / "feature.py"
    src_file.parent.mkdir(parents=True, exist_ok=True)
    src_file.write_text("def test(): pass\n", encoding="utf-8")
    
    src_snap = snapshots_dir / "feature.py.snap"
    src_snap.write_text("def test(): pass\n", encoding="utf-8")
    
    red_snap = snapshots_dir / "red.txt.snap"
    red_snap.write_text("AssertionError: red failed", encoding="utf-8")
    green_snap = snapshots_dir / "green.txt.snap"
    green_snap.write_text("PASSED", encoding="utf-8")
    regr_snap = snapshots_dir / "regression.txt.snap"
    regr_snap.write_text("PASSED", encoding="utf-8")
    
    manifest_file = root / "artifacts" / "candidate_manifest.json"
    manifest_file.write_text(json.dumps({
        "candidate_id": "cand-001",
        "files": [
            {"path": "src/feature.py", "snapshot": "artifacts/snapshots/feature.py.snap"},
            {"path": "artifacts/evidence/red.txt", "snapshot": "artifacts/snapshots/red.txt.snap"},
            {"path": "artifacts/evidence/green.txt", "snapshot": "artifacts/snapshots/green.txt.snap"},
            {"path": "artifacts/evidence/regression.txt", "snapshot": "artifacts/snapshots/regression.txt.snap"},
        ]
    }), encoding="utf-8")
    
    # 5. task card
    card_path = iter_dir / "task-01.md"
    card_content = """---
schema_version: "1"
delivery_mode: filesystem
task_id: "task-01"
type: "Strict-TDD"
candidate_id: "cand-001"
status: "DONE"
review_status: "APPROVED"
tdd_verified: "true"
review_receipt: "artifacts/review_receipt.json"
---

<!-- iter:scope -->
| 文件路径 |
| :--- |
| `src/feature.py` |
<!-- /iter:scope -->

<!-- iter:acceptance -->
- [x] 功能实现并通过全部测试
<!-- /iter:acceptance -->

<!-- iter:ledger -->
Ledger content
<!-- /iter:ledger -->
"""
    card_path.write_text(card_content, encoding="utf-8")
    
    contract_snap = snapshots_dir / "task-01.snap.md"
    contract_snap.write_text(card_content, encoding="utf-8")
    
    # 6. review receipt
    receipt_file = root / "artifacts" / "review_receipt.json"
    receipt_file.write_text(json.dumps({
        "schema_version": 1,
        "receipt_kind": "current-filesystem-review-v1",
        "delivery_mode": "filesystem",
        "task_id": "task-01",
        "type": "Strict-TDD",
        "task_path": "docs/todos/01-test-iter/task-01.md",
        "candidate_id": "cand-001",
        "verdict": "APPROVED",
        "recorded_at": "2026-11-12T03:00:00+00:00",
        "implementer": "alice",
        "reviewer": "bob",
        "review_report": "artifacts/review_report.md",
        "candidate_manifest": "artifacts/candidate_manifest.json",
        "contract_snapshot": "artifacts/snapshots/task-01.snap.md",
        "goal_snapshot": "artifacts/snapshots/goal_snap.md",
        "checks": [
            {
                "name": "red",
                "kind": "command",
                "command": "pytest -k red",
                "cwd": ".",
                "exit_code": 1,
                "failure_kind": "assertion",
                "summary": "red assertion failure",
                "output": "artifacts/evidence/red.txt"
            },
            {
                "name": "green",
                "kind": "command",
                "command": "pytest -k green",
                "cwd": ".",
                "exit_code": 0,
                "summary": "green passes",
                "output": "artifacts/evidence/green.txt"
            },
            {
                "name": "regression",
                "kind": "command",
                "command": "pytest",
                "cwd": ".",
                "exit_code": 0,
                "summary": "regression passes",
                "output": "artifacts/evidence/regression.txt"
            }
        ]
    }), encoding="utf-8")
    
    return card_path


def create_fs_fixture_with_empty_files(tmp_path: Path):
    """Fixture containing both 0-byte file scope and 0-byte file under directory scope."""
    root = tmp_path
    iter_dir = root / "docs" / "todos" / "01-test-iter"
    iter_dir.mkdir(parents=True, exist_ok=True)

    delivery_cfg = iter_dir / "iteration-delivery.json"
    delivery_cfg.write_text(json.dumps({
        "schema_version": 1,
        "mode": "filesystem"
    }), encoding="utf-8")

    readme_content = """# Iteration 01
<!-- iter:goal -->
迭代核心目标与全局约束：验证纯文件系统交付收据能力。
<!-- /iter:goal -->
"""
    (iter_dir / "README.md").write_text(readme_content, encoding="utf-8")

    snapshots_dir = root / "artifacts" / "snapshots"
    evidence_dir = root / "artifacts" / "evidence"
    snapshots_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)

    goal_snap = snapshots_dir / "goal_snap.md"
    goal_snap.write_text(readme_content, encoding="utf-8")

    check_red = evidence_dir / "red.txt"
    check_red.write_text("AssertionError: red failed", encoding="utf-8")
    check_green = evidence_dir / "green.txt"
    check_green.write_text("PASSED", encoding="utf-8")
    check_regression = evidence_dir / "regression.txt"
    check_regression.write_text("PASSED", encoding="utf-8")

    report_file = root / "artifacts" / "review_report.md"
    report_file.write_text("LGTM approved", encoding="utf-8")

    # Scoped direct file: 0-byte empty.txt
    empty_file = root / "src" / "empty.txt"
    empty_file.parent.mkdir(parents=True, exist_ok=True)
    empty_file.write_bytes(b"")

    empty_snap = snapshots_dir / "empty.txt.snap"
    empty_snap.write_bytes(b"")

    # Scoped directory: pkg/ containing 0-byte stderr.log and non-empty code.py
    pkg_dir = root / "pkg"
    pkg_dir.mkdir(parents=True, exist_ok=True)
    code_file = pkg_dir / "code.py"
    code_file.write_text("print('hello')\n", encoding="utf-8")
    stderr_file = pkg_dir / "stderr.log"
    stderr_file.write_bytes(b"")

    code_snap = snapshots_dir / "code.py.snap"
    code_snap.write_text("print('hello')\n", encoding="utf-8")
    stderr_snap = snapshots_dir / "stderr.log.snap"
    stderr_snap.write_bytes(b"")

    red_snap = snapshots_dir / "red.txt.snap"
    red_snap.write_text("AssertionError: red failed", encoding="utf-8")
    green_snap = snapshots_dir / "green.txt.snap"
    green_snap.write_text("PASSED", encoding="utf-8")
    regr_snap = snapshots_dir / "regression.txt.snap"
    regr_snap.write_text("PASSED", encoding="utf-8")

    manifest_file = root / "artifacts" / "candidate_manifest.json"
    manifest_file.write_text(json.dumps({
        "candidate_id": "cand-001",
        "files": [
            {"path": "src/empty.txt", "snapshot": "artifacts/snapshots/empty.txt.snap"},
            {"path": "pkg/code.py", "snapshot": "artifacts/snapshots/code.py.snap"},
            {"path": "pkg/stderr.log", "snapshot": "artifacts/snapshots/stderr.log.snap"},
            {"path": "artifacts/evidence/red.txt", "snapshot": "artifacts/snapshots/red.txt.snap"},
            {"path": "artifacts/evidence/green.txt", "snapshot": "artifacts/snapshots/green.txt.snap"},
            {"path": "artifacts/evidence/regression.txt", "snapshot": "artifacts/snapshots/regression.txt.snap"},
        ]
    }), encoding="utf-8")

    card_path = iter_dir / "task-01.md"
    card_content = """---
schema_version: "1"
delivery_mode: filesystem
task_id: "task-01"
type: "Strict-TDD"
candidate_id: "cand-001"
status: "DONE"
review_status: "APPROVED"
tdd_verified: "true"
review_receipt: "artifacts/review_receipt.json"
---

<!-- iter:scope -->
| 文件路径 |
| :--- |
| `src/empty.txt` |
| `pkg/` |
<!-- /iter:scope -->

<!-- iter:acceptance -->
- [x] 功能实现并通过全部测试
<!-- /iter:acceptance -->

<!-- iter:ledger -->
Ledger content
<!-- /iter:ledger -->
"""
    card_path.write_text(card_content, encoding="utf-8")

    contract_snap = snapshots_dir / "task-01.snap.md"
    contract_snap.write_text(card_content, encoding="utf-8")

    receipt_file = root / "artifacts" / "review_receipt.json"
    receipt_file.write_text(json.dumps({
        "schema_version": 1,
        "receipt_kind": "current-filesystem-review-v1",
        "delivery_mode": "filesystem",
        "task_id": "task-01",
        "type": "Strict-TDD",
        "task_path": "docs/todos/01-test-iter/task-01.md",
        "candidate_id": "cand-001",
        "verdict": "APPROVED",
        "recorded_at": "2026-11-12T03:00:00+00:00",
        "implementer": "alice",
        "reviewer": "bob",
        "review_report": "artifacts/review_report.md",
        "candidate_manifest": "artifacts/candidate_manifest.json",
        "contract_snapshot": "artifacts/snapshots/task-01.snap.md",
        "goal_snapshot": "artifacts/snapshots/goal_snap.md",
        "checks": [
            {
                "name": "red",
                "kind": "command",
                "command": "pytest -k red",
                "cwd": ".",
                "exit_code": 1,
                "failure_kind": "assertion",
                "summary": "red assertion failure",
                "output": "artifacts/evidence/red.txt"
            },
            {
                "name": "green",
                "kind": "command",
                "command": "pytest -k green",
                "cwd": ".",
                "exit_code": 0,
                "summary": "green passes",
                "output": "artifacts/evidence/green.txt"
            },
            {
                "name": "regression",
                "kind": "command",
                "command": "pytest",
                "cwd": ".",
                "exit_code": 0,
                "summary": "regression passes",
                "output": "artifacts/evidence/regression.txt"
            }
        ]
    }), encoding="utf-8")

    return card_path


def test_positive_filesystem_audit(tmp_path):
    card_path = create_synthetic_fs_fixture(tmp_path)
    res = audit_task_file(card_path)
    assert res["is_valid_done"] is True, f"audit failed: {res}"


def test_empty_scope_and_snapshot_files_allowed(tmp_path):
    """0-byte source and snapshot files in scope/manifest must pass binding."""
    card_path = create_fs_fixture_with_empty_files(tmp_path)
    res = audit_task_file(card_path)
    assert res["is_valid_done"] is True, f"audit failed on legal empty files: {res}"


def test_empty_scope_source_with_drifted_snapshot_rejected(tmp_path):
    """0-byte source vs non-empty snapshot must be rejected for mismatch."""
    card_path = create_fs_fixture_with_empty_files(tmp_path)
    snap = tmp_path / "artifacts" / "snapshots" / "empty.txt.snap"
    snap.write_text("drifted content", encoding="utf-8")
    res = audit_task_file(card_path)
    assert res["is_valid_done"] is False
    assert any("Source and snapshot content mismatch: src/empty.txt" in err for err in res["violations"])


def test_check_output_empty_still_rejected(tmp_path):
    """check.output must NOT allow empty file."""
    card_path = create_fs_fixture_with_empty_files(tmp_path)
    (tmp_path / "artifacts" / "evidence" / "green.txt").write_bytes(b"")
    (tmp_path / "artifacts" / "snapshots" / "green.txt.snap").write_bytes(b"")
    res = audit_task_file(card_path)
    assert res["is_valid_done"] is False
    assert any("Missing or empty evidence artifact: artifacts/evidence/green.txt" in err for err in res["violations"])


def test_review_report_empty_still_rejected(tmp_path):
    """review_report must NOT allow empty file."""
    card_path = create_fs_fixture_with_empty_files(tmp_path)
    (tmp_path / "artifacts" / "review_report.md").write_bytes(b"")
    res = audit_task_file(card_path)
    assert res["is_valid_done"] is False
    assert any("Missing or empty evidence artifact: artifacts/review_report.md" in err for err in res["violations"])
