import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from iter_contracts import TYPE_CHECKS, contract_projection, parse_card, scope_paths
from iter_templates import render_task_card, validate_generated_card
from iter_filesystem import validate_filesystem_binding


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


@pytest.mark.parametrize("task_type", TYPE_CHECKS)
@pytest.mark.parametrize("mode", ["git", "filesystem"])
def test_cli_roundtrip(task_type, mode, tmp_path):
    script = Path(__file__).resolve().parents[1] / "scripts/iter_templates.py"
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec_for(task_type, mode)), encoding="utf-8")
    result = subprocess.run([sys.executable, "-B", str(script), "--render", str(spec_path)], capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0
    assert result.stdout == render_task_card(spec_for(task_type, mode))
    card = tmp_path / "card.md"
    card.write_text(result.stdout, encoding="utf-8")
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    result = subprocess.run([sys.executable, "-B", str(script), "--check", str(card), "--delivery-mode", mode], capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0
    assert json.loads(result.stdout) == {"valid": True, "errors": []}
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}


@pytest.mark.parametrize("text", ["{key: value}", "List<T>", "<details>text</details>", "Discuss TODO state", "```python\nx = {'a': 1}\n```"])
def test_legitimate_notation(text):
    spec = spec_for()
    spec["objective"] = text
    assert validate_generated_card(render_task_card(spec), "git") == []


@pytest.mark.parametrize("text", ["{{task_name}}", "${TASK_ID}", "{TODO}", "{TBD}", "YYYY-MM-DD"])
def test_explicit_placeholders(text):
    spec = spec_for()
    spec["objective"] = text
    with pytest.raises(ValueError):
        render_task_card(spec)
    card = render_task_card(spec_for()).replace("Generate typed cards", text)
    assert validate_generated_card(card, "git")


@pytest.mark.parametrize("field", sorted(spec_for()))
def test_required_spec_fields(field):
    spec = spec_for()
    del spec[field]
    with pytest.raises(ValueError):
        render_task_card(spec)


@pytest.mark.parametrize("changes", [
    {"objective": []}, {"task_id": 2}, {"scope": "src/"}, {"scope": [2]},
    {"scope": ["C:/outside"]}, {"scope": [".git/config"]}, {"scope": ["/absolute"]},
    {"scope": ["src/*.py"]}, {"stages": [""]}, {"acceptance": {}},
    {"verification": []}, {"verification": {"red": "", "green": "run", "regression": "run"}},
    {"candidate_id": "unexpected"}, {"delivery_mode": "filesystem", "candidate_id": ""},
])
def test_spec_shapes_and_paths(changes):
    spec = spec_for()
    spec.update(changes)
    with pytest.raises(ValueError):
        render_task_card(spec)


@pytest.mark.parametrize("old,new", [
    ('schema_version: 1', 'schema_version: 2'),
    ('task_id: "02"', 'task_id: "{{task_id}}"'),
    ('type: "Strict-TDD"', 'type: "Other"'),
    ('status: "TODO"', 'status: "TODO"\nunknown: "value"'),
    ('**red**：Run the actual red check', '**red**：'),
    ('| `scripts/example.py` |', '| `../outside` |'),
])
def test_generated_card_boundaries(old, new):
    assert validate_generated_card(render_task_card(spec_for()).replace(old, new), "git")


@pytest.mark.parametrize("key", ["base_sha", "head_sha", "contract_sha"])
def test_filesystem_rejects_sha(key):
    card = render_task_card(spec_for(mode="filesystem"))
    card = card.replace(f'{key}: ""', f'{key}: "abc"') if f'{key}:' in card else card.replace('schema_version: 1', f'schema_version: 1\n{key}: "abc"')
    assert validate_generated_card(card, "filesystem")


def test_cli_invalid_inputs(tmp_path):
    script = Path(__file__).resolve().parents[1] / "scripts/iter_templates.py"
    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    for args in (["--render", str(bad)], ["--check", str(bad), "--delivery-mode", "git"], ["--check", str(tmp_path / "missing"), "--delivery-mode", "filesystem"]):
        result = subprocess.run([sys.executable, "-B", str(script), *args], capture_output=True, text=True, encoding="utf-8")
        assert result.returncode == 2
        assert json.loads(result.stdout)["valid"] is False


@pytest.mark.parametrize("mode", ["git", "filesystem"])
def test_missing_sections_and_mode_boundaries(mode):
    card = render_task_card(spec_for(mode=mode))
    for name in ("scope", "stages", "acceptance", "verification", "ledger"):
        broken = card.replace(f"<!-- iter:{name} -->", f"<!-- removed:{name} -->")
        assert validate_generated_card(broken, mode)
    assert validate_generated_card(card, "filesystem" if mode == "git" else "git")
    if mode == "filesystem":
        assert validate_generated_card(card.replace('candidate_id: "candidate-02-a"', 'candidate_id: ""'), mode)
    else:
        assert validate_generated_card(card.replace('schema_version: 1', 'schema_version: 1\ncandidate_id: "unexpected"'), mode)


@pytest.mark.parametrize("task_type", TYPE_CHECKS)
def test_actual_filesystem_freeze_binding(task_type, tmp_path):
    spec = spec_for(task_type, "filesystem")
    spec["scope"] = ["source.py"]
    card = render_task_card(spec)
    task_path = "docs/todos/01-example/02-task.md"
    goal = "<!-- iter:goal -->\nFrozen iteration goal\n<!-- /iter:goal -->\n"
    files = {task_path: card, "docs/todos/01-example/README.md": goal,
             "source.py": "source = 1\n", "frozen/source.py": "source = 1\n",
             "frozen/card.md": card, "frozen/goal.md": goal,
             "frozen/manifest.json": json.dumps({"candidate_id": spec["candidate_id"], "files": [{"path": "source.py", "snapshot": "frozen/source.py"}]})}
    for name, text in files.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    # Binding-only fixture: no verdict, approval, historical RED or review receipt is fabricated.
    binding = {"candidate_manifest": "frozen/manifest.json", "contract_snapshot": "frozen/card.md", "goal_snapshot": "frozen/goal.md"}
    meta = parse_card(card)[0]
    assert validate_filesystem_binding(meta, binding, tmp_path, task_path, card) == []
    registered = card.replace('status: "TODO"', 'status: "TESTING"')
    assert validate_filesystem_binding(parse_card(registered)[0], binding, tmp_path, task_path, registered) == []
    for changed in (card.replace("- [ ] Implement behavior", "- [x] Implement behavior"), card.replace("实际命令、", "已运行命令、")):
        assert any("contract_snapshot projection mismatch" in e for e in validate_filesystem_binding(meta, binding, tmp_path, task_path, changed))
    changed_binding = dict(binding)
    (tmp_path / "frozen/manifest.json").write_text(json.dumps({"candidate_id": "different", "files": [{"path": "source.py", "snapshot": "frozen/source.py"}]}), encoding="utf-8")
    assert any("candidate_id mismatch" in e for e in validate_filesystem_binding(meta, changed_binding, tmp_path, task_path, card))


def test_git_projection_keeps_existing_mutability():
    card = render_task_card(spec_for())
    changed = card.replace("- [ ] Implement behavior", "- [x] Implement behavior").replace("实际命令、", "已运行命令、")
    assert contract_projection(card) == contract_projection(changed)
