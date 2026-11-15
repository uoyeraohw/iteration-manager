"""New-card guidance and existing type gates; no business approval is implied."""
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from iter_contracts import TYPE_CHECKS
from iter_templates import render_task_card, validate_generated_card
from test_template_generation import spec_for

CHECKS = ("baseline", "regression", "compatibility", "benchmark_before", "benchmark_after")


def test_policy_preserves_target_distinction_and_existing_guards():
    policy = (ROOT / "references/refactor_evidence.md").read_text(encoding="utf-8")
    contract = (ROOT / "templates/contracts/refactor_benchmark_contract.md").read_text(encoding="utf-8")
    assert tuple(TYPE_CHECKS["Refactor-Benchmark"]) == CHECKS
    assert len(TYPE_CHECKS) == 4
    for text in (policy, contract):
        assert "性能" in text and "结构" in text and "UNKNOWN/BLOCKED" in text
        assert "baseline" in text and "regression" in text and "compatibility" in text
    assert "各三次" in policy and "合成" in policy
    card = render_task_card(spec_for("Refactor-Benchmark"))
    assert "references/refactor_evidence.md" in card
    assert validate_generated_card(card, "git") == []


@pytest.mark.parametrize("missing", CHECKS)
def test_each_required_check_rejected_in_spec_and_card(missing):
    spec = spec_for("Refactor-Benchmark")
    del spec["verification"][missing]
    with pytest.raises(ValueError, match="exactly"):
        render_task_card(spec)
    card = render_task_card(spec_for("Refactor-Benchmark"))
    line = f"- [ ] **{missing}**：Run the actual {missing} check\n"
    assert line in card
    assert any(missing in e for e in validate_generated_card(card.replace(line, ""), "git"))


@pytest.mark.parametrize("missing", CHECKS)
def test_receipt_rejects_each_missing_check(tmp_path, missing):
    from iter_contracts import validate_receipt
    (tmp_path / "evidence.txt").write_text("synthetic shape fixture", encoding="utf-8")
    meta = dict(task_id="01", type="Refactor-Benchmark", base_sha="base", head_sha="head", review_status="APPROVED")
    checks = []
    for name in CHECKS:
        check = dict(name=name, kind="observation" if name == "compatibility" else "command",
                     summary="fixture only", output="evidence.txt")
        if name != "compatibility":
            check.update(command="example", cwd=".", exit_code=0)
        checks.append(check)
    receipt = dict(schema_version=1, task_id="01", type="Refactor-Benchmark", task_path="card.md",
                   base_sha="base", head_sha="head", contract_sha="head", implementer="a", reviewer="b",
                   verdict="APPROVED", review_report="evidence.txt", checks=checks)
    assert validate_receipt(meta, receipt, tmp_path, "card.md") == []
    receipt["checks"] = [check for check in checks if check["name"] != missing]
    assert f"Missing required check: {missing}" in validate_receipt(meta, receipt, tmp_path, "card.md")
