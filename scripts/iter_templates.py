"""Pure task-card generation; no project files or state are written."""
import argparse
import json
import re
import sys
from pathlib import Path

from iter_contracts import TYPE_CHECKS, contract_projection, parse_card, relative_path, scope_paths, section


_REQUIRED = {
    "version", "task_id", "iteration", "task_name", "type", "delivery_mode",
    "objective", "consumes", "produces", "scope", "stages", "acceptance", "verification",
}
_PLACEHOLDER = re.compile(r"\{\{\s*[\w.-]+\s*\}\}|\$\{[\w.-]+\}|\{(?:TODO|TBD)\}|YYYY-MM-DD")
_META_FIELDS = {
    "schema_version", "iteration", "task_id", "task_name", "status", "type",
    "fix_rounds", "replan_count", "is_blocked", "blocked_reason", "typesafe_score",
    "typesafe_evidence", "tdd_verified", "review_status", "review_receipt",
    "base_sha", "head_sha", "contract_sha", "delivery_mode", "candidate_id",
}
_TYPE_GUIDANCE = {
    "Strict-TDD": "核心行为先取得可编译测试的真实断言RED，再最小GREEN；环境错误不算RED。",
    "UI-Component": "先走真实用户路径，再检查正常、空、加载、错误四态及约定视口和实际视觉。",
    "Refactor-Benchmark": "保持外部行为与接口；同环境同数据量取得benchmark_before与benchmark_after实测。",
    "Spike-Discovery": "隔离实验，保留可复查决定与后续接口，不虚构测试或批准。",
}


def _text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text")
    if _PLACEHOLDER.search(value):
        raise ValueError(f"Unresolved placeholder in {name}")
    return value


def _validate_spec(spec):
    if not isinstance(spec, dict):
        raise ValueError("spec must be an object")
    allowed = _REQUIRED | {"candidate_id"}
    if set(spec) - allowed or _REQUIRED - set(spec):
        raise ValueError("Unknown or missing spec fields")
    if type(spec["version"]) is not int or spec["version"] != 1:
        raise ValueError("Unsupported spec version")
    for name in _REQUIRED - {"version", "scope", "stages", "acceptance", "verification"}:
        _text(spec[name], name)
    if spec["type"] not in TYPE_CHECKS:
        raise ValueError("Unknown task type")
    if spec["delivery_mode"] not in ("git", "filesystem"):
        raise ValueError("Unknown delivery_mode")
    if spec["delivery_mode"] == "filesystem":
        _text(spec.get("candidate_id"), "candidate_id")
    elif "candidate_id" in spec:
        raise ValueError("candidate_id is only valid for filesystem delivery")
    for name in ("scope", "stages", "acceptance"):
        if not isinstance(spec[name], list) or not spec[name]:
            raise ValueError(f"{name} must be a nonempty array")
        for value in spec[name]:
            _text(value, name)
            if name == "scope":
                relative_path(value)
                if any(char in value for char in "|`\r\n"):
                    raise ValueError("scope path cannot contain Markdown delimiters")
    checks = spec["verification"]
    if not isinstance(checks, dict) or set(checks) != set(TYPE_CHECKS[spec["type"]]):
        raise ValueError("verification must contain exactly the required type checks")
    for name, value in checks.items():
        _text(value, f"verification.{name}")


def _checklist(name, values):
    return f"<!-- iter:{name} -->\n" + "\n".join(f"- [ ] {value}" for value in values) + f"\n<!-- /iter:{name} -->"


def render_task_card(spec: dict) -> str:
    """Render a new schema1 card, rejecting invalid specs with ValueError."""
    _validate_spec(spec)
    meta = {
        "schema_version": 1, "iteration": spec["iteration"], "task_id": spec["task_id"],
        "task_name": spec["task_name"], "status": "TODO", "type": spec["type"],
        "fix_rounds": 0, "replan_count": 0, "is_blocked": False, "blocked_reason": "",
        "typesafe_score": "UNASSESSED", "typesafe_evidence": "", "tdd_verified": False,
        "review_status": "PENDING", "review_receipt": "", "base_sha": "", "head_sha": "",
    }
    if spec["delivery_mode"] == "filesystem":
        meta.update(delivery_mode="filesystem", candidate_id=spec["candidate_id"])
    front = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in meta.items())
    scope = "\n".join(f"| `{relative_path(path)}` | MODIFIED | 本任务授权范围 |" for path in spec["scope"])
    verification = [f"**{name}**：{spec['verification'][name]}" for name in TYPE_CHECKS[spec["type"]]]
    mode_rule = (
        "完整正文、阶段勾选及实证先定稿，再冻结候选并独审；审查后只登记允许的元数据及外部收据，正文变化须重新冻结与受影响重审。"
        if spec["delivery_mode"] == "filesystem" else
        "提交实现C及原始证据，再独立审查冻结规格；主管登记D后运行strict，head_sha绑定C。"
    )
    return f"""---
{front}
---

# {spec['task_id']} · {spec['task_name']}

## 1. 任务执行目标与接口契约
- **主要目标**：{spec['objective']}
- **Consumes**：{spec['consumes']}
- **Produces**：{spec['produces']}

## 2. 业务阶段
{_checklist('stages', spec['stages'])}

## 3. 按类型验证规划
{_TYPE_GUIDANCE[spec['type']]}
{_checklist('verification', verification)}

## 4. 交付与冻结
{mode_rule}
执行状态与审查结果读取frontmatter及review_receipt；生成不代表验证或独立批准。

## 5. 新增或变更内容清单
<!-- iter:scope -->
| 文件路径 | 变更类型 | 核心职责说明 |
| --- | --- | --- |
{scope}
<!-- /iter:scope -->

## 6. 确定性验收标准
{_checklist('acceptance', spec['acceptance'])}

## 7. 执行实证与裁决账本
<!-- iter:ledger -->
实际命令、原始证据、退出码、候选、检查点与剩余项在执行中记录；未执行不推断通过。
独立审查结果由外部收据与报告提供。
<!-- /iter:ledger -->
"""


def validate_generated_card(content: str, delivery_mode: str) -> list[str]:
    """Precheck a newly generated card, not a completion/review receipt."""
    if delivery_mode not in ("git", "filesystem"):
        return ["Unknown delivery_mode"]
    meta, body, errors = parse_card(content)
    errors = list(errors)
    if set(meta) - _META_FIELDS:
        errors.append("Unknown generated-card metadata")
    if any(_PLACEHOLDER.search(value) for value in meta.values()):
        errors.append("Unresolved placeholder in metadata")
    expected = {"schema_version": "1", "status": "TODO", "review_status": "PENDING",
                "tdd_verified": "false", "typesafe_score": "UNASSESSED"}
    for name, value in expected.items():
        if meta.get(name) != value:
            errors.append(f"Invalid initial {name}")
    for name in ("task_id", "iteration", "task_name"):
        if not meta.get(name, "").strip():
            errors.append(f"Missing {name}")
    checks = TYPE_CHECKS.get(meta.get("type"))
    if checks is None:
        errors.append("Unknown task type")
    errors.extend(scope_paths(content)[1])
    try:
        contract_projection(content)
    except ValueError as exc:
        errors.append(str(exc))
    for name in ("stages", "acceptance", "verification"):
        block = section(content, name, r"(?!)")
        if block is None or not re.search(r"^- \[ \] \S", block, re.M):
            errors.append(f"Missing {name} checklist")
    for name in checks or ():
        block = section(content, "verification", r"(?!)") or ""
        if not re.search(r"^- \[ \] \*\*" + re.escape(name) + r"\*\*：\S[^\n]*", block, re.M):
            errors.append(f"Missing required check: {name}")
    if _PLACEHOLDER.search(body):
        errors.append("Unresolved placeholder in body")
    if delivery_mode == "filesystem":
        if meta.get("delivery_mode") != "filesystem" or not meta.get("candidate_id", "").strip():
            errors.append("Filesystem mode and candidate_id required")
        if any(meta.get(key, "").strip() for key in ("base_sha", "head_sha", "contract_sha")):
            errors.append("Filesystem cards cannot contain SHA values")
    elif meta.get("delivery_mode", "git") != "git":
        errors.append("Delivery mode mismatch")
    elif "candidate_id" in meta:
        errors.append("candidate_id is only valid for filesystem delivery")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--render", metavar="SPEC_JSON")
    action.add_argument("--check", metavar="CARD_MD")
    parser.add_argument("--delivery-mode", choices=("git", "filesystem"))
    args = parser.parse_args(argv)
    try:
        if args.render:
            if args.delivery_mode is not None:
                raise ValueError("--render uses delivery_mode from the spec")
            content = render_task_card(json.loads(Path(args.render).read_text(encoding="utf-8")))
            errors = validate_generated_card(content, parse_card(content)[0].get("delivery_mode", "git"))
            if errors:
                raise ValueError("; ".join(errors))
            sys.stdout.write(content)
            return 0
        if args.delivery_mode is None:
            raise ValueError("--check requires --delivery-mode")
        errors = validate_generated_card(Path(args.check).read_text(encoding="utf-8"), args.delivery_mode)
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False))
    return 2 if errors else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
