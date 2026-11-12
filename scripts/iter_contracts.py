"""Pure, standard-library task card parsing and evidence contracts."""
import json
import re
from pathlib import Path, PurePosixPath

STATUSES = {
    "TODO": ("TODO", "⚪ 待开始", "⚪ 待开始 (TODO)"),
    "IN_PROGRESS": ("IN_PROGRESS", "🟡 进行中", "🟡 进行中 (IN_PROGRESS)"),
    "TESTING": ("TESTING", "🔵 待验收", "🔵 待验收 (TESTING)"),
    "DONE": ("DONE", "🟢 已完成", "🟢 已完成 (DONE)"),
    "FUSED": ("FUSED", "🔴 已熔断", "🔴 已熔断 (FUSED)"),
}


def parse_card(content):
    """Read flat frontmatter only; body examples never supply metadata."""
    match = re.match(r"\A\ufeff?---[^\S\n]*\n(.*?)\n---[^\S\n]*(?:\n|$)", content, re.S)
    meta, errors = {}, []
    if not match:
        return {}, content, ["Missing or unterminated frontmatter"]
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        field = re.fullmatch(r"([a-z_][a-z0-9_]*):\s*(.*?)\s*", line)
        if not field:
            errors.append(f"Unsupported frontmatter line: {line}")
            continue
        key, raw = field.groups()
        if key in meta:
            errors.append(f"Duplicate frontmatter key: {key}")
        if raw.startswith('"'):
            try:
                value, end = json.JSONDecoder().raw_decode(raw)
                if raw[end:].strip() and not raw[end:].lstrip().startswith("#"):
                    raise ValueError("Trailing content")
                if not isinstance(value, str):
                    raise ValueError("Expected text")
            except ValueError:
                errors.append(f"Invalid quoted value: {key}")
                value = raw
        elif raw.startswith("'"):
            quoted = re.fullmatch(r"'((?:[^']|'')*)'\s*(?:#.*)?", raw)
            value = quoted.group(1).replace("''", "'") if quoted else raw
            if not quoted:
                errors.append(f"Invalid quoted value: {key}")
        else:
            value = re.split(r"\s+#", raw, maxsplit=1)[0].strip()
        meta[key] = value
    if meta.get("schema_version", "0") not in ("0", "1"):
        errors.append("Unsupported schema_version")
    return meta, content[match.end():], errors


def card_status(content):
    meta, _, _ = parse_card(content)
    value = meta.get("status", "")
    return next((name for name, aliases in STATUSES.items() if value in aliases), "UNKNOWN")


def section(content, name, legacy_title):
    begin, end = f"<!-- iter:{name} -->", f"<!-- /iter:{name} -->"
    if begin in content or end in content:
        if content.count(begin) != 1 or content.count(end) != 1:
            return None
        rest = content.split(begin, 1)[1]
        return rest.split(end, 1)[0] if end in rest else None
    match = re.search(r"^##\s+[^\n]*(?:" + legacy_title + r")[^\n]*\n(.*?)(?=^##\s|\Z)",
                      content, re.M | re.S)
    return match.group(1) if match else None


def relative_path(value):
    value = value.replace("\\", "/")
    p = PurePosixPath(value)
    if (not value or value.startswith("/") or re.match(r"^[A-Za-z]:", value)
            or ".." in p.parts or value in (".", "./") or ":" in value
            or any(part == ".git" for part in p.parts) or any(c in value for c in "*?[]")):
        raise ValueError(f"Expected a repository-relative path: {value!r}")
    return p.as_posix() + ("/" if value.endswith("/") else "")


def scope_paths(content):
    block = section(content, "scope", "新增或变更|File & Scope Impact")
    if block is None:
        return [], ["Missing or malformed scope section"]
    paths, errors = [], []
    for line in block.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        value = line.strip().split("|")[1].strip().strip("`")
        if value in ("文件路径", "File", "File path", "Path") or re.fullmatch(r"[:\-\s]+", value):
            continue
        try:
            path = relative_path(value)
            if path not in paths:
                paths.append(path)
        except ValueError as e:
            errors.append(str(e))
    if not paths:
        errors.append("Empty scope whitelist")
    return paths, errors


TYPE_CHECKS = {
    "Strict-TDD": ("red", "green", "regression"),
    "UI-Component": ("interaction", "states", "visual", "regression"),
    "Refactor-Benchmark": ("baseline", "regression", "compatibility", "benchmark_before", "benchmark_after"),
    "Spike-Discovery": ("experiment", "decision", "interfaces"),
}
OBSERVATIONS = {"states", "visual", "compatibility", "decision", "interfaces"}


def contained(root, value, directory=False, allow_empty=False):
    """Resolve symlinks too; an artifact must actually stay inside the project."""
    if not isinstance(value, str):
        raise ValueError("Artifact path must be text")
    rel = "." if directory and value == "." else relative_path(value)
    path = (root / rel).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Path leaves repository: {value}")
    if directory:
        if not path.is_dir():
            raise ValueError(f"Missing cwd directory: {value}")
    elif not path.is_file() or (not allow_empty and not path.stat().st_size):
        raise ValueError(f"Missing or empty evidence artifact: {value}")
    return path


from datetime import datetime


def _has_valid_iso_tz(val: object) -> bool:
    """Return True if val is a valid ISO 8601 string with timezone offset."""
    if not isinstance(val, str) or not val.strip():
        return False
    try:
        dt = datetime.fromisoformat(val)
        return dt.utcoffset() is not None
    except (ValueError, TypeError):
        return False


def validate_receipt(meta, receipt, root, task_path, delivery='git'):
    """Validate shape, not the semantic truth of a review or test output."""
    errors = []
    if not isinstance(receipt, dict):
        return ["Receipt must be a JSON object"]
    if type(receipt.get("schema_version")) is not int or receipt["schema_version"] != 1:
        errors.append("Unsupported receipt schema_version")

    is_fs = delivery == 'filesystem'

    if is_fs:
        for key in ("task_id", "type", "candidate_id"):
            expected = meta.get(key)
            if not isinstance(expected, str) or not expected.strip() or receipt.get(key) != expected:
                errors.append(f"Receipt {key} mismatch or missing")
        if receipt.get("task_path") != task_path:
            errors.append("Receipt task_path mismatch or missing")
        if meta.get("delivery_mode") != "filesystem" or receipt.get("delivery_mode") != "filesystem":
            errors.append("Filesystem delivery mode required in meta and receipt")
        if receipt.get("receipt_kind") != "current-filesystem-review-v1":
            errors.append("Invalid receipt_kind for filesystem delivery")
        if not _has_valid_iso_tz(receipt.get("recorded_at")):
            errors.append("Receipt recorded_at must be valid ISO timestamp with timezone")
        for obj_name, obj in (("meta", meta), ("receipt", receipt)):
            for sha_key in ("base_sha", "head_sha", "contract_sha"):
                val = obj.get(sha_key)
                if val is not None and str(val).strip():
                    errors.append(f"Unexpected SHA {sha_key} present in {obj_name} under filesystem mode")
        for key in ("implementer", "reviewer"):
            val = receipt.get(key)
            if not isinstance(val, str) or not val.strip() or val != val.strip():
                errors.append(f"Missing receipt {key}")
    else:
        for key, expected in (("task_id", meta.get("task_id")), ("type", meta.get("type")),
                              ("task_path", task_path), ("base_sha", meta.get("base_sha")),
                              ("head_sha", meta.get("head_sha"))):
            if not expected or receipt.get(key) != expected:
                errors.append(f"Receipt {key} mismatch or missing")
        for key in ("implementer", "reviewer", "contract_sha"):
            if not isinstance(receipt.get(key), str) or not receipt[key].strip():
                errors.append(f"Missing receipt {key}")

    if receipt.get("implementer") == receipt.get("reviewer"):
        errors.append("Reviewer must be independent of implementer")
    if receipt.get("verdict") != "APPROVED" or meta.get("review_status") != "APPROVED":
        errors.append("Independent review APPROVED required")
    if meta.get("type") == "Strict-TDD" and meta.get("tdd_verified", "").lower() != "true":
        errors.append("Strict-TDD requires tdd_verified: true")
    try:
        contained(root, receipt.get("review_report"))
    except (OSError, ValueError) as e:
        errors.append(str(e))
    required = TYPE_CHECKS.get(meta.get("type"))
    if not required:
        errors.append("Unknown task type")
    checks = receipt.get("checks")
    if not isinstance(checks, list):
        return errors + ["Missing checks array"]
    seen = set()
    for check in checks:
        if not isinstance(check, dict) or not isinstance(check.get("name"), str):
            errors.append("Invalid check object/name")
            continue
        name = check["name"]
        if name in seen:
            errors.append(f"Duplicate check: {name}")
        seen.add(name)
        if not isinstance(check.get("summary"), str) or not check["summary"].strip():
            errors.append(f"Missing summary: {name}")
        try:
            contained(root, check.get("output"))
            allow_fs_ui_obs = is_fs and meta.get("type") == "UI-Component" and name == "interaction"
            expected_kind = "observation" if name in OBSERVATIONS else "command"
            kind = check.get("kind")

            if allow_fs_ui_obs and kind == "observation":
                if not isinstance(check.get("source_tool"), str) or not check["source_tool"].strip():
                    raise ValueError(f"Missing source_tool for filesystem UI observation: {name}")
                if not _has_valid_iso_tz(check.get("observed_at")):
                    raise ValueError(f"Missing or invalid timezone in observed_at: {name}")
            else:
                if kind != expected_kind:
                    raise ValueError(f"Invalid check kind: {name}")
                if expected_kind == "command":
                    if not isinstance(check.get("command"), str) or not check["command"].strip():
                        raise ValueError(f"Missing command: {name}")
                    contained(root, check.get("cwd"), directory=True)
                    code = check.get("exit_code")
                    if type(code) is not int:
                        raise ValueError(f"Integer exit_code required: {name}")
                    if name == "red":
                        if code == 0 or check.get("failure_kind") != "assertion":
                            raise ValueError("RED requires nonzero assertion failure, not environment/compile error")
                    elif code != 0:
                        raise ValueError(f"Successful command required: {name}")
        except (OSError, ValueError) as e:
            errors.append(str(e))
    for name in required or ():
        if name not in seen:
            errors.append(f"Missing required check: {name}")
    return errors


MUTABLE_METADATA = {
    "status", "stage_current", "stage_progress", "fix_rounds", "replan_count", "is_blocked",
    "blocked_reason", "tdd_verified", "review_status", "base_sha", "head_sha", "review_receipt", "updated_at", "autonomy_state",
}


def contract_projection(content):
    """Only execution metadata, checklist marks and the exact ledger are mutable."""
    meta, body, errors = parse_card(content)
    if errors:
        raise ValueError("Invalid frozen task card: " + "; ".join(errors))
    for name in ("scope", "acceptance", "ledger"):
        if section(body, name, r"(?!)") is None:
            raise ValueError(f"schema1 requires paired iter:{name} markers")
    body = re.sub(r"<!-- iter:ledger -->.*?<!-- /iter:ledger -->", "", body, flags=re.S)
    body = re.sub(r"^(> \*\*(?:当前状态|当前阶段|TypeSafe 质检分)\*\*：)[^\n]*", r"\1", body, flags=re.M)
    body = re.sub(r"(\-\s*\[)[xX ](\])", r"\1 \2", body)
    return {k: v for k, v in meta.items() if k not in MUTABLE_METADATA}, body


def matches_scope(path, scopes):
    return any(path == p or (p.endswith("/") and path.startswith(p)) for p in scopes)


def validate_binding(meta, receipt, root, task_path, content, git, resolve):
    """Bind the contract, code and raw evidence to immutable Git versions."""
    errors = []
    refs = {}
    for key in ("base_sha", "head_sha", "contract_sha"):
        value = receipt.get(key)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value):
            raise ValueError(f"Full commit required: {key}")
        refs[key] = resolve(value, root)
    base, head, contract = (refs[k] for k in ("base_sha", "head_sha", "contract_sha"))
    current = resolve("HEAD", root)
    for ancestor, descendant in ((base, head), (contract, head), (head, current)):
        if git(["merge-base", ancestor, descendant], root).strip() != ancestor:
            errors.append(f"Invalid commit ancestry: {ancestor} -> {descendant}")
    frozen = git(["show", contract + ":" + task_path], root)
    reviewed = git(["show", head + ":" + task_path], root)
    expected = contract_projection(frozen)
    if contract_projection(reviewed) != expected or contract_projection(content) != expected:
        errors.append("Task contract drift after frozen specification; affected re-review required")
    readme = (PurePosixPath(task_path).parent / "README.md").as_posix()
    goal_title = "迭代核心目标与全局约束|Iteration Goal.*Global Constraints"
    goals = [section(git(["show", ref + ":" + readme], root), "goal", goal_title)
             for ref in (contract, head)]
    goals.append(section((root / readme).read_text(encoding="utf-8"), "goal", goal_title))
    if goals[0] is None or any(goal != goals[0] for goal in goals[1:]):
        errors.append("Missing or drifted iteration goal/global constraints")
    scopes, scope_errors = scope_paths(frozen)
    errors += scope_errors
    # Both new artifacts may be registered after C; existing artifacts remain immutable.
    registration = {relative_path(meta["review_receipt"]), relative_path(receipt["review_report"])}
    exempt = {path for path in registration
              if not git(["ls-tree", "-r", "--name-only", head, "--", path], root).strip()}
    implicit = {task_path, readme}
    changes = [p for p in git(["diff", "--no-renames", "--name-only", "-z", base, head, "--"], root).split("\0") if p]
    for path in changes:
        if path not in implicit and not matches_scope(path, scopes):
            errors.append(f"Reviewed implementation outside frozen scope: {path}")
    later = [p for p in git(["diff", "--no-renames", "--name-only", "-z", head, current, "--"], root).split("\0") if p]
    for args in (["diff", "--name-only", "--no-renames", "-z", "--"],
                 ["diff", "--cached", "--name-only", "--no-renames", "-z", "--"],
                 ["ls-files", "--others", "--exclude-standard", "-z"]):
        later += [p for p in git(args, root).split("\0") if p]
    for path in sorted(set(later)):
        if path not in implicit | exempt and matches_scope(path, scopes):
            errors.append(f"Scoped file drift after reviewed implementation: {path}")
    for check in receipt["checks"]:
        path = relative_path(check["output"])
        if not git(["ls-tree", "-r", "--name-only", head, "--", path], root).strip():
            errors.append(f"Raw evidence absent from reviewed commit: {path}")
        if not matches_scope(path, scopes):
            errors.append(f"Evidence outside task scope: {path}")
    return errors
