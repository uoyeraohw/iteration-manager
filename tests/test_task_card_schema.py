import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from iter_sync import extract_section_4_whitelist, scan_task_file


def test_current_template_scope_is_readable():
    template = Path(__file__).resolve().parents[1] / "templates/task_detail.md"
    assert extract_section_4_whitelist(template) == [
        "src/modules/example.js", "src/routes/api.js", "test/modules/example.test.js",
        "docs/todos/{迭代序号}-{迭代名称}/evidence/{任务序号}/"]


def test_status_is_exact_and_confined_to_frontmatter(tmp_path):
    card = tmp_path / "01-task.md"
    card.write_text('---\nstatus: NOT_DONE\n---\n', encoding="utf-8")
    assert scan_task_file(card) == "UNKNOWN"
    card.write_text('# Task\n```yaml\nstatus: DONE\n```\n', encoding="utf-8")
    assert scan_task_file(card) == "UNKNOWN"
