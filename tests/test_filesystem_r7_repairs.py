"""Tests for filesystem delivery mode R7 repairs and hardenings."""
import http.client
import http.server
import threading
from pathlib import Path
import pytest

from test_filesystem_delivery_controller import dump, fixture
from iter_sync import (
    audit_task_file,
    generate_board_data,
    sync_local_iteration,
    LiveBoardHandler,
)
from iter_filesystem import load_profile
from iter_contracts import contract_projection


def serve(directory):
    handler = type("BoundHandler", (LiveBoardHandler,), {"iter_dir": directory})
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def request(server, path, headers=None):
    conn = http.client.HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
    req_headers = {"Host": f"127.0.0.1:{server.server_address[1]}"}
    if headers:
        req_headers.update(headers)
    conn.request("GET", path, headers=req_headers)
    resp = conn.getresponse()
    result = (resp.status, dict(resp.getheaders()), resp.read())
    conn.close()
    return result


def test_profile_derivation_missing_and_unknown_keys(tmp_path):
    card, _, _ = fixture(tmp_path, "Strict-TDD")
    it_dir = card.parent

    # 1. Valid profile derives project root
    assert load_profile(it_dir) == tmp_path

    # 2. Missing profile returns None
    profile_file = it_dir / "iteration-delivery.json"
    profile_file.unlink()
    assert load_profile(it_dir) is None

    # 3. Unknown key in profile must be rejected by load_profile / audit
    dump(profile_file, {"schema_version": 1, "mode": "filesystem", "unexpected_extra_key": "bad"})
    with pytest.raises(ValueError):
        load_profile(it_dir)
    assert audit_task_file(card)["verdict"] == "FAIL"

    # 4. Boolschema checks: boolean values for non-bool or invalid types rejected
    dump(profile_file, {"schema_version": True, "mode": "filesystem"})
    with pytest.raises(ValueError):
        load_profile(it_dir)
    assert audit_task_file(card)["verdict"] == "FAIL"


def test_fs_board_sources_contain_exact_evidence_and_checks(tmp_path):
    card, receipt, _ = fixture(tmp_path, "Strict-TDD")
    it_dir = card.parent

    board = generate_board_data(it_dir)
    assert board["accepted"] == 1
    card_entry = next(c for c in board["cards"] if c["id"] == "01")

    expected_sources = {
        "evidence/review.json",
        "evidence/review.txt",
        "evidence/red.txt",
        "evidence/green.txt",
        "evidence/regression.txt",
    }
    actual_sources = {s["path"] for s in card_entry["sources"]}
    assert actual_sources == expected_sources
    assert len(card_entry["sources"]) == len(expected_sources)


def test_live_board_evidence_http_serving(tmp_path):
    card, receipt, _ = fixture(tmp_path, "Strict-TDD")
    it_dir = card.parent
    server, thread = serve(it_dir)
    try:
        board = generate_board_data(it_dir)
        card_entry = next(c for c in board["cards"] if c["id"] == "01")
        sources = card_entry["sources"]
        expected_sources = {
            "evidence/review.json",
            "evidence/review.txt",
            "evidence/red.txt",
            "evidence/green.txt",
            "evidence/regression.txt",
        }
        assert {s["path"] for s in sources} == expected_sources

        for index, src in enumerate(sources):
            status, _, body = request(server, f"/api/evidence?task=01-task.md&source={index}")
            assert status == 200
            expected_bytes = (tmp_path / src["path"]).read_bytes()
            assert body == expected_bytes
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_unknown_profile_key_blanks_board_and_returns_404(tmp_path):
    card, _, _ = fixture(tmp_path, "Strict-TDD")
    it_dir = card.parent
    dump(it_dir / "iteration-delivery.json", {
        "schema_version": 1,
        "mode": "filesystem",
        "forbidden_key": "fail",
    })

    audit = audit_task_file(card)
    assert audit["verdict"] == "FAIL"

    board = generate_board_data(it_dir)
    assert len(board.get("cards", [])) > 0
    for card_entry in board["cards"]:
        assert card_entry.get("sources") == []

    server, thread = serve(it_dir)
    try:
        status, _, _ = request(server, "/api/evidence?task=01-task.md&source=0")
        assert status == 404
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


@pytest.mark.parametrize("drift_kind", ["ledger_replace", "uncheck_acceptance", "append_visible_status"])
def test_fs_body_drift_fails_audit(tmp_path, drift_kind):
    card, _, _ = fixture(tmp_path, "Strict-TDD")
    original_text = card.read_text(encoding="utf-8")
    snapshot_path = tmp_path / "frozen/contract.md"

    if drift_kind == "ledger_replace":
        modified_text = original_text.replace("Synthetic ledger", "Tampered ledger text")
        card.write_text(modified_text, encoding="utf-8")
        assert audit_task_file(card)["verdict"] != "PASS"

    elif drift_kind == "uncheck_acceptance":
        modified_text = original_text.replace("- [x] Synthetic acceptance", "- [ ] Synthetic acceptance")
        card.write_text(modified_text, encoding="utf-8")
        assert audit_task_file(card)["verdict"] != "PASS"

    elif drift_kind == "append_visible_status":
        baseline_line = "\n> **当前状态**：基线\n"
        baseline_card = original_text + baseline_line
        card.write_text(baseline_card, encoding="utf-8")
        snapshot_path.write_text(baseline_card, encoding="utf-8")
        assert audit_task_file(card)["verdict"] == "PASS"

        drifted_card = original_text + "\n> **当前状态**：改变\n"
        card.write_text(drifted_card, encoding="utf-8")
        assert audit_task_file(card)["verdict"] == "FAIL"


def test_fs_contract_metadata_mutability(tmp_path):
    card, _, _ = fixture(tmp_path, "Strict-TDD")
    original = card.read_text(encoding="utf-8")

    # 1. Immutable metadata alteration rejected
    bad_candidate = original.replace("candidate_id: synthetic-current-1", "candidate_id: tampered-cand-9")
    card.write_text(bad_candidate, encoding="utf-8")
    assert audit_task_file(card)["verdict"] != "PASS"

    # 2. Allowed mutable metadata alteration accepted
    card.write_text(original, encoding="utf-8")
    assert audit_task_file(card)["verdict"] == "PASS"
    updated_card = original.replace(
        "delivery_mode: filesystem\n",
        'delivery_mode: filesystem\nupdated_at: "2026-11-12T04:00:00+00:00"\n',
    )
    card.write_text(updated_card, encoding="utf-8")
    assert audit_task_file(card)["verdict"] == "PASS"


def test_git_contract_projection_ignores_dynamic_fields(tmp_path):
    card, _, _ = fixture(tmp_path, "Strict-TDD")
    base_text = card.read_text(encoding="utf-8") + "\n> **当前状态**：基线\n"

    modified_text = base_text
    if "status: DONE" in modified_text:
        modified_text = modified_text.replace("status: DONE", "status: IN_PROGRESS")
    elif "status: ACCEPTED" in modified_text:
        modified_text = modified_text.replace("status: ACCEPTED", "status: IN_PROGRESS")
    else:
        modified_text = modified_text.replace("status: IN_PROGRESS", "status: DONE")

    modified_text = modified_text.replace("- [x] Synthetic acceptance", "- [ ] Synthetic acceptance")
    modified_text = modified_text.replace("Synthetic ledger", "Synthetic ledger\nLog appended")
    modified_text = modified_text.replace("> **当前状态**：基线", "> **当前状态**：改变")

    proj1 = contract_projection(base_text)
    proj2 = contract_projection(modified_text)
    assert proj1 == proj2


@pytest.mark.parametrize("whitespace_variant", [
    ("synthetic-author ", "synthetic-reviewer"),
    (" synthetic-author", "synthetic-reviewer"),
    ("\tsynthetic-author", "synthetic-reviewer"),
    ("synthetic-author\n", "synthetic-reviewer"),
    ("synthetic-author", "synthetic-reviewer "),
    ("synthetic-author", " synthetic-reviewer"),
    ("synthetic-author", "\tsynthetic-reviewer"),
    ("synthetic-author", "synthetic-reviewer\n"),
    ("synthetic-author", "synthetic-author "),
])
def test_fs_identities_whitespace_rejected(tmp_path, whitespace_variant):
    card, receipt, _ = fixture(tmp_path, "Strict-TDD")
    receipt_path = tmp_path / "evidence/review.json"

    # Baseline: clean, independent identities PASS
    assert audit_task_file(card)["verdict"] == "PASS"

    imp, rev = whitespace_variant
    receipt["implementer"] = imp
    receipt["reviewer"] = rev
    dump(receipt_path, receipt)

    audit = audit_task_file(card)
    assert audit["verdict"] != "PASS"


def test_fs_empty_inventory_maintains_empty_status(tmp_path):
    it_dir = tmp_path / "docs/todos/01-empty"
    it_dir.mkdir(parents=True)
    dump(it_dir / "iteration-delivery.json", {"schema_version": 1, "mode": "filesystem"})
    (it_dir / "README.md").write_text("# Empty Iteration\n", encoding="utf-8")

    result = sync_local_iteration(it_dir, dry_run=True, strict=True)
    assert result.get("total", 0) == 0
    assert result.get("gate_violations") == []
    assert result.get("conclusion") == "EMPTY"
    assert result.get("status") == "暂无任务"
