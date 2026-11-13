import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from iter_contracts import TYPE_CHECKS, contract_projection, parse_card, scope_paths
from iter_templates import render_task_card, validate_generated_card


def spec_for(task_type="Strict-TDD", mode="git"):
    spec = dict(version=1, task_id="02", iteration="10-example",
                task_name="Generate typed cards", type=task_type, delivery_mode=mode,
                objective="Render a task card without side effects",
                consumes="TYPE_CHECKS", produces="render_task_card(spec) -> str",
                scope=["scripts/example.py", "tests/"], stages=["Implement behavior"],
                acceptance=["Generated card is readable"],
                verification={name: f"Run the actual {name} check" for name in TYPE_CHECKS[task_type]})
    if mode == "filesystem":
        spec["candidate_id"] = "candidate-02-a"
    return spec


@pytest.mark.parametrize("task_type", TYPE_CHECKS)
@pytest.mark.parametrize("mode", ["git", "filesystem"])
def test_render_core_combinations(task_type, mode):
    spec = spec_for(task_type, mode)
    before = copy.deepcopy(spec)
    content = render_task_card(spec)
    meta, body, errors = parse_card(content)
    assert errors == [], "render must produce parseable schema1 frontmatter"
    assert meta["schema_version"] == "1"
    assert meta["type"] == task_type
    assert meta["status"] == "TODO"
    assert meta["review_status"] == "PENDING"
    assert meta["tdd_verified"] == "false"
    assert meta["typesafe_score"] == "UNASSESSED"
    assert scope_paths(content) == (spec["scope"], [])
    contract_projection(content)
    for name in TYPE_CHECKS[task_type]:
        assert f"**{name}**" in body
        assert spec["verification"][name] in body
    assert validate_generated_card(content, mode) == []
    assert spec == before
    assert render_task_card(spec) == content
    if mode == "filesystem":
        assert meta["candidate_id"] == "candidate-02-a"
        assert all(not meta.get(key) for key in ("base_sha", "head_sha", "contract_sha"))
        assert "完整正文" in body and "冻结" in body
        assert "PENDING" not in body
    if task_type != "Strict-TDD":
        assert "RED" not in body


@pytest.mark.parametrize("changes", [
    {"version": 2}, {"version": True}, {"type": "Other"}, {"extra": "unknown"},
    {"scope": []}, {"scope": ["../escape.py"]}, {"objective": "{TODO}"},
    {"verification": {}}, {"acceptance": []}, {"delivery_mode": "other"},
])
def test_reject_invalid_spec(changes):
    spec = spec_for()
    spec.update(changes)
    with pytest.raises(ValueError):
        render_task_card(spec)


def test_check_rejects_empty_card_and_unknown_mode():
    assert validate_generated_card("", "git")
    assert validate_generated_card("", "other")
