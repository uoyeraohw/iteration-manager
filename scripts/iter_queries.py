"""Read-only task discovery, audit and handoff queries; no CLI dependency."""
import json
import re
import subprocess
from pathlib import Path
from iter_autonomy import load_state
from iter_filesystem import load_profile, validate_filesystem_binding
from iter_contracts import (card_status, parse_card, scope_paths, contained,
                            validate_receipt, validate_binding, section)


def _run_git(args: list, cwd: Path) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git"] + args, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", check=False)
    except OSError as e:
        return subprocess.CompletedProcess(["git"] + args, 127, "", str(e))


def _checked_git(args: list, cwd: Path) -> str:
    result = _run_git(args, cwd)
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed ({result.returncode}): {result.stderr.strip()}")
    return result.stdout


def resolve_commit(ref: str, cwd: Path) -> str:
    value = _checked_git(["rev-parse", "--verify", "--end-of-options", ref + "^{commit}"], cwd).strip()
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value):
        raise ValueError(f"Invalid commit: {ref}")
    return value


def discover_task_files(directory: Path, read_root: Path | None = None) -> list[Path]:
    """Keep identifiable or unreadable cards; exclude unmarked support documents."""
    task_files = []
    for path in sorted(directory.glob("*.md")):
        # Opt-in reports retain unsafe candidates as errors without reading them,
        # including nonnumeric names whose metadata cannot safely be inspected.
        if (read_root is not None and path.name.lower() != "readme.md"
                and not path.resolve().is_relative_to(read_root)):
            task_files.append(path)
            continue
        if not path.is_file() or path.name.lower() == "readme.md":
            continue
        if re.match(r"^\d+", path.name):
            task_files.append(path)
            continue
        try:
            meta, _, _ = parse_card(path.read_text(encoding="utf-8"))
            if "task_id" in meta or "status" in meta:
                task_files.append(path)
        except (OSError, UnicodeError):
            task_files.append(path)
    return task_files


def audit_task_file(file_path: Path) -> dict:
    """Compatibility entry point for declared state plus completion evidence."""
    status, errors, verdict = "UNKNOWN", [], "UNKNOWN"
    try:
        content = file_path.read_text(encoding="utf-8")
        meta, _, parse_errors = parse_card(content)
        errors.extend(parse_errors)
        status = card_status(content)

        iter_dir = file_path.resolve().parent
        fs_root = load_profile(iter_dir)

        if status == "FUSED":
            errors.append("BLOCKED: Task is FUSED")
            verdict = "BLOCKED"
        elif status == "UNKNOWN":
            errors.append("UNKNOWN: missing or invalid status")
        elif status == "DONE":
            is_fs_card = meta.get("delivery_mode") == "filesystem"
            if fs_root is not None:
                if not is_fs_card:
                    errors.append("Filesystem profile present but task delivery_mode is not filesystem")
            else:
                if is_fs_card:
                    errors.append("Task declared filesystem delivery_mode but iteration delivery profile is missing")

            if meta.get("schema_version") != "1" or not meta.get("review_receipt"):
                errors += ["UNKNOWN: legacy or missing schema_version", "UNKNOWN: missing review_receipt; do not synthesize approval"]
            else:
                if fs_root is not None:
                    root = fs_root
                    delivery_mode = "filesystem"
                else:
                    root = Path(_checked_git(["rev-parse", "--show-toplevel"], file_path.parent).strip()).resolve()
                    delivery_mode = "git"

                task_path = file_path.resolve().relative_to(root).as_posix()
                receipt_path = contained(root, meta["review_receipt"])
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                errors += validate_receipt(meta, receipt, root, task_path, delivery=delivery_mode)
                if not errors:
                    if delivery_mode == "filesystem":
                        errors += validate_filesystem_binding(meta, receipt, root, task_path, content)
                    else:
                        errors += validate_binding(meta, receipt, root, task_path, content, _checked_git, resolve_commit)
                acceptance = section(content, "acceptance", "确定性验收标准|Acceptance Criteria")
                if not acceptance or not re.search(r"^\s*-\s*\[[xX]\]", acceptance, re.M) or re.search(r"^\s*-\s*\[\s\]", acceptance, re.M):
                    errors.append("Missing or incomplete acceptance checklist")
                verdict = "FAIL" if errors else "PASS"
    except (OSError, UnicodeError, ValueError, RuntimeError) as error:
        errors.append(str(error))
        verdict = "FAIL"
    return {"file": file_path.name, "status": status, "is_valid_done": status == "DONE" and verdict == "PASS",
            "verdict": verdict, "violations": errors}


def render_task_envelope(task_file: Path, repo_dir: Path) -> dict:
    """Read-only handoff: declarations, actual audit and persistent budgets stay distinct."""
    return _render_task_envelope(task_file, repo_dir, audit_task_file)


def _render_task_envelope(task_file: Path, repo_dir: Path, audit_task):
    try:
        content = task_file.read_text(encoding="utf-8")
        meta, _, errors = parse_card(content)
        state = load_state(meta)
        audit = audit_task(task_file)
        status = card_status(content)
        micro = parse_task_stages_and_micro_state(content, status)
        projection = task_handoff_projection(task_file, meta, state)
        changed = []
        if meta.get("base_sha") and meta.get("head_sha"):
            try:
                base = resolve_commit(meta["base_sha"], repo_dir)
                head = resolve_commit(meta["head_sha"], repo_dir)
                changed = [p for p in _checked_git(["diff", "--name-only", "-z", base, head, "--"], repo_dir).split("\0") if p]
            except (RuntimeError, ValueError) as error:
                errors.append(str(error))
        return {"TASK_HANDOFF": dict(
            schema_version=1, task_id=meta.get("task_id", task_file.stem),
            **projection,
            task_name=meta.get("task_name", task_file.stem), type=meta.get("type", "UNKNOWN"),
            status=status, commit_sha=meta.get("head_sha", ""), base_sha=meta.get("base_sha", ""),
            fix_rounds=state["round"], fix_total=state["total"], consilium_count=state["consilium"],
            replan_count=state["replan"], writer=state["writer"], blocked_reason=state["blocked_reason"],
            is_blocked=bool(state["blocked_reason"]) or status == 'FUSED', review_status=meta.get("review_status", "PENDING"),
            acceptance_verdict=audit["verdict"], evidence={"receipt":meta.get("review_receipt", "")},
            errors=errors+audit["violations"], files_changed_count=len(changed), files_changed=changed,
            stage_current=micro["stage_current"], stage_progress=micro["stage_progress"])}
    except (OSError, ValueError, TypeError) as error:
        return {"error": str(error)}



def parse_task_stages_and_micro_state(content: str, st: str) -> dict:
    """Derive business progress only from the checklist, never declared status."""
    meta, _, errors = parse_card(content)
    try:
        state = load_state(meta)
    except (ValueError, TypeError) as error:
        state = dict(round=None, total=None, consilium=None, replan=None, policy={},
                     blocked_reason=str(error))
        errors.append(str(error))
    def checklist(block):
        result = []
        for line in (block or "").splitlines():
            match = re.match(r"^\s*-\s*\[([ xX])\]\s*(.+)$", line)
            if match:
                text = match[2].replace("**", "").strip()
                result.append(dict(title=text, full_text=match[2], done=match[1].lower()=="x"))
        return result
    stages = checklist(section(content, "stages", "业务阶段|Execution Stages|里程碑"))
    steps = checklist(section(content, "verification", "按类型验证规划|Verification Process|TDD|红绿循环"))
    count = len(stages)
    done = sum(s["done"] for s in stages)
    current = next((s["title"] for s in stages if not s["done"]), "阶段清单已勾选完毕" if count else "UNKNOWN")
    step = next((s["title"] for s in steps if not s["done"]), "CHECKLIST_COMPLETE (未等同验收)" if steps else "UNKNOWN")
    pct = round(done/count*100, 1) if count else None
    reason = '; '.join(dict.fromkeys(v for v in (meta.get('blocked_reason',''),state['blocked_reason']) if v))
    blocked = bool(reason) or st == "FUSED" or meta.get("is_blocked","").lower() == "true"
    if blocked and not reason:
        reason = "任务声明阻塞，未记录具体恢复条件"
    return dict(stage_current=current, stage_progress=f"{done}/{count} ({pct:g}%)" if count else "UNKNOWN",
                stage_pct=pct, stages_done=done, stages_total=count, stages=stages,
                tdd_step=step, tdd_steps=steps, replan_count=state["replan"], fix_rounds=state["round"],
                fix_total=state["total"], consilium_count=state["consilium"], policy=state["policy"],
                is_blocked=blocked, blocked_reason=reason, errors=errors)




def task_handoff_projection(task_file: Path, meta: dict, state: dict) -> dict:
    """Fields shared by board and envelope, without cross-call state."""
    from iter_execution import execution_summary
    fs_root = load_profile(task_file.resolve().parent)
    mode = 'filesystem' if fs_root is not None and meta.get('delivery_mode') == 'filesystem' else (
        'UNKNOWN' if meta.get('delivery_mode') == 'filesystem' or fs_root is not None else 'git')
    return dict(delivery_mode=mode,
                candidate_id=meta.get('candidate_id', '') if mode == 'filesystem' else '',
                execution=execution_summary(state))
