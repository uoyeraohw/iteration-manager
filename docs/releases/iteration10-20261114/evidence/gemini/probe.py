"""Probe for Gemini installation consumption verification.

Executes controlled checks against installed iteration-manager scripts:
1. Constructs and validates UI-Component/filesystem spec.json.
2. Renders card.md with iter_templates.py --render and checks with --check.
3. Tests scope traversal rejection with ['../escape'] via iter_templates.py.
4. Runs iter_sync.py --takeover-report against iteration 10 docs and verifies 6 DONE/PASS tasks.
5. Saves probe-results.json with exact execution details.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

INSTALL_ROOT = Path("C:/Users/qingyu/.gemini/config/skills/iteration-manager").resolve()
ITER_TEMPLATES = INSTALL_ROOT / "scripts" / "iter_templates.py"
ITER_SYNC = INSTALL_ROOT / "scripts" / "iter_sync.py"
CWD = Path.cwd().resolve()

results = []

def run_step(name, argv):
    print(f"[*] Running {name}: {' '.join(argv)}")
    proc = subprocess.run(
        argv,
        cwd=str(CWD),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    record = {
        "name": name,
        "argv": argv,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }
    results.append(record)
    return proc

def main():
    print(f"CWD: {CWD}")
    print(f"INSTALL_ROOT: {INSTALL_ROOT}")
    assert INSTALL_ROOT.is_dir(), f"Install root {INSTALL_ROOT} not found"
    assert ITER_TEMPLATES.is_file(), f"{ITER_TEMPLATES} not found"
    assert ITER_SYNC.is_file(), f"{ITER_SYNC} not found"

    # Step 1: Construct UI-Component / filesystem spec.json
    spec = {
        "version": 1,
        "task_id": "01",
        "iteration": "10-self-hosting-hardening",
        "task_name": "UI组件安装消费验证",
        "type": "UI-Component",
        "delivery_mode": "filesystem",
        "candidate_id": "安装消费隔离样例",
        "objective": "验证 UI-Component filesystem 渲染与检查 (ITER10-GEMINI-20261114)",
        "consumes": "TYPE_CHECKS",
        "produces": "card.md",
        "scope": ["src/ui/component.py", "tests/ui/"],
        "stages": [
            "阶段一：构建组件",
            "阶段二：验证交付"
        ],
        "acceptance": [
            "UI 四类验收齐备，marker 为 ITER10-GEMINI-20261114"
        ],
        "verification": {
            "interaction": "点击按钮触发相应交互事件并记录观测",
            "states": "正常态、空态、加载态、错误态四态齐备",
            "visual": "遵循设计规范样式与视口尺寸要求",
            "regression": "原有UI测试集全量回归无损"
        }
    }

    spec_file = CWD / "spec.json"
    spec_file.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[+] Saved {spec_file}")
    results.append({
        "name": "save_spec",
        "argv": ["internal:save_spec", str(spec_file)],
        "returncode": 0,
        "stdout": f"Saved spec.json with marker ITER10-GEMINI-20261114, candidate_id: {spec['candidate_id']}",
        "stderr": ""
    })

    # Step 2: Call iter_templates.py --render spec.json
    proc_render = run_step(
        "render_card",
        [sys.executable, "-B", str(ITER_TEMPLATES), "--render", str(spec_file)]
    )
    assert proc_render.returncode == 0, f"render failed with code {proc_render.returncode}: {proc_render.stderr}"
    card_content = proc_render.stdout
    card_file = CWD / "card.md"
    card_file.write_text(card_content, encoding="utf-8")
    print(f"[+] Saved {card_file}")

    # Assertions on card content
    assert "status: \"TODO\"" in card_content, "card status must be TODO"
    assert "review_status: \"PENDING\"" in card_content, "review_status must be PENDING"
    assert "tdd_verified: false" in card_content, "tdd_verified must be false"
    assert "candidate_id: \"安装消费隔离样例\"" in card_content, "candidate_id must match"
    for check_key in ("interaction", "states", "visual", "regression"):
        assert f"**{check_key}**：" in card_content, f"card must contain verification check for {check_key}"
    assert "RED" not in card_content.split("## 3. 按类型验证规划")[1].split("## 4. 交付与冻结")[0], "UI-Component must not synthesize RED"
    assert "GREEN" not in card_content.split("## 3. 按类型验证规划")[1].split("## 4. 交付与冻结")[0], "UI-Component must not synthesize GREEN"

    # Call iter_templates.py --check card.md --delivery-mode filesystem
    proc_check = run_step(
        "check_card",
        [sys.executable, "-B", str(ITER_TEMPLATES), "--check", str(card_file), "--delivery-mode", "filesystem"]
    )
    assert proc_check.returncode == 0, f"check failed with code {proc_check.returncode}: {proc_check.stderr}"
    check_json = json.loads(proc_check.stdout)
    assert check_json.get("valid") is True, f"card validation failed: {check_json}"
    assert check_json.get("errors") == [], f"card validation errors: {check_json.get('errors')}"

    # Step 3: Test scope traversal rejection with ['../escape']
    escape_spec = dict(spec)
    escape_spec["scope"] = ["../escape"]
    escape_spec_file = CWD / "spec_escape.json"
    escape_spec_file.write_text(json.dumps(escape_spec, ensure_ascii=False, indent=2), encoding="utf-8")

    proc_escape = run_step(
        "render_escape_scope",
        [sys.executable, "-B", str(ITER_TEMPLATES), "--render", str(escape_spec_file)]
    )
    assert proc_escape.returncode == 2, f"Expected returncode 2 for escape scope, got {proc_escape.returncode}"
    # The output from iter_templates on error is JSON printed to stdout
    try:
        escape_err_json = json.loads(proc_escape.stdout)
        assert escape_err_json.get("valid") is False, f"Expected valid=false: {escape_err_json}"
        assert len(escape_err_json.get("errors", [])) > 0, "Expected at least one error message"
        print(f"[+] Verified scope traversal error: {escape_err_json['errors']}")
    except Exception as exc:
        raise AssertionError(f"Could not parse escape render error as JSON: {proc_escape.stdout}") from exc

    # Verify no escaped file was created
    escaped_target = (CWD.parent / "escape")
    assert not escaped_target.exists(), f"Out-of-bounds file should not exist: {escaped_target}"

    # Step 4: Run iter_sync.py --takeover-report C:/Users/qingyu/.codeg/skills/iteration-manager/docs/todos/10-self-hosting-hardening
    target_iter_dir = Path("C:/Users/qingyu/.codeg/skills/iteration-manager/docs/todos/10-self-hosting-hardening")
    proc_takeover = run_step(
        "takeover_report",
        [sys.executable, "-B", str(ITER_SYNC), "--takeover-report", str(target_iter_dir)]
    )
    assert proc_takeover.returncode == 0, f"takeover report failed: {proc_takeover.stderr}"
    takeover_file = CWD / "takeover.json"
    takeover_file.write_text(proc_takeover.stdout, encoding="utf-8")
    print(f"[+] Saved {takeover_file}")

    takeover_data = json.loads(proc_takeover.stdout)
    assert takeover_data.get("read_only") is True, f"takeover report must have read_only=True: {takeover_data}"
    tasks = takeover_data.get("tasks", [])
    assert len(tasks) == 6, f"Expected 6 tasks, found {len(tasks)}"
    for t in tasks:
        assert t.get("declared_status") == "DONE", f"Task {t.get('path')} declared_status must be DONE, got {t.get('declared_status')}"
        assert t.get("acceptance_verdict") == "PASS", f"Task {t.get('path')} acceptance_verdict must be PASS, got {t.get('acceptance_verdict')}"
    print(f"[+] All 6 tasks declared DONE and acceptance_verdict PASS verified.")

    # Save probe-results.json
    results_file = CWD / "probe-results.json"
    results_file.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[+] Saved {results_file}")
    print("[*] All probe assertions passed successfully!")

if __name__ == "__main__":
    main()
