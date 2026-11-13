import http.server
import socketserver
import threading
import webbrowser
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iteration Manager v2.1 - Global & Local Status Aggregation, SDD Review Packager,
Scope Firewall, Task Handoff Envelope, Circuit Breaker & Heterogeneous Consilium Engine (iter_sync.py)

Provides deterministic, zero-dependency, conflict-free eventual consistency
synchronization, scope isolation and Superpowers SDD governance for docs/todos/ across multi-worktree Git branches.
"""

import os
import re
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
from iter_autonomy import load_state, record_event
from iter_filesystem import load_profile, validate_filesystem_binding
from iter_contracts import (card_status, parse_card, scope_paths, relative_path, contained,
                            validate_receipt, validate_binding, matches_scope, section)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


STATUS_BADGE_MAP = {
    "DONE": "🟢 已完成",
    "IN_PROGRESS": "🟡 进行中",
    "TESTING": "🔵 待验收",
    "TODO": "⚪ 待开始",
    "FUSED": "🔴 已熔断",
}


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


def worktree_changed_files(cwd: Path) -> list:
    """Read-only inventory; staged and unstaged changes cannot cancel each other."""
    paths = set()
    for args in (["diff", "--name-only", "--no-renames", "-z", "--"],
                 ["diff", "--cached", "--name-only", "--no-renames", "-z", "--"],
                 ["ls-files", "--others", "--exclude-standard", "-z"]):
        paths.update(p for p in _checked_git(args, cwd).split("\0") if p)
    return sorted(paths)


def committed_candidate_errors(path: Path) -> list:
    try:
        root = Path(_checked_git(["rev-parse", "--show-toplevel"], path).strip()).resolve()
        dirty = worktree_changed_files(root)
        return ["Uncommitted candidate changes: " + ", ".join(dirty)] if dirty else []
    except (OSError, ValueError, RuntimeError) as error:
        return [str(error)]


def scan_task_file(file_path: Path) -> str:
    """Read an exact declared state; missing/unknown metadata stays UNKNOWN."""
    try:
        return card_status(file_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        return "UNKNOWN"


def extract_section_4_whitelist(task_file: Path) -> list:
    """Compatibility name: semantic scope, including legacy section 4/5 tables."""
    try:
        return scope_paths(task_file.read_text(encoding="utf-8"))[0]
    except (OSError, UnicodeError):
        return []


def audit_scope_firewall(repo_dir: Path, base_sha: str, head_sha: str, task_file: Path,
                         include_worktree: bool = False, baseline_dirty=None) -> dict:
    """Check the declared scope without editing, staging or reverting any file."""
    changed, whitelist, violations = [], [], []
    preexisting = []
    try:
        root = Path(_checked_git(["rev-parse", "--show-toplevel"], repo_dir).strip()).resolve()
        task = task_file if task_file.is_absolute() else root / task_file
        rel = task.resolve().relative_to(root).as_posix()
        whitelist, violations = scope_paths(task.read_text(encoding="utf-8"))
        whitelist += [rel, task.parent.resolve().relative_to(root).as_posix() + "/README.md"]
        base, head = resolve_commit(base_sha, root), resolve_commit(head_sha, root)
        changed = [p for p in _checked_git(["diff", "--no-renames", "--name-only", "-z", base, head, "--"], root).split("\0") if p]
        if include_worktree:
            changed = sorted(set(changed) | set(worktree_changed_files(root)))
        if baseline_dirty is not None:
            if not isinstance(baseline_dirty, list) or not all(isinstance(p, str) for p in baseline_dirty):
                raise ValueError("baseline-dirty must be a JSON array of relative paths")
            preexisting = sorted(set(map(relative_path, baseline_dirty)) & set(changed))
        for path in changed:
            if path == ".git" or path.startswith(".git/") or not (root / path).resolve().is_relative_to(root):
                violations.append(f"Path leaves repository or touches Git metadata: {path}")
            elif not any(path == w or (w.endswith("/") and path.startswith(w)) for w in whitelist):
                violations.append(f"Unapproved file outside scope whitelist: {path}")
    except (OSError, UnicodeError, ValueError, RuntimeError) as error:
        violations.append(str(error))
    return {"passed": not violations, "violations": violations, "changed_files": changed,
            "whitelist": whitelist, "preexisting_files": preexisting}


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
        from iter_execution import execution_summary
        execution = execution_summary(state)
        fs_root = load_profile(task_file.resolve().parent)
        mode = 'filesystem' if fs_root is not None and meta.get('delivery_mode') == 'filesystem' else (
            'UNKNOWN' if meta.get('delivery_mode') == 'filesystem' or fs_root is not None else 'git')
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
            delivery_mode=mode, candidate_id=meta.get('candidate_id', '') if mode == 'filesystem' else '',
            execution=execution,
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



def record_fix_and_check_fuse(task_file: Path, repo_dir: Path, error_summary: str = "",
                              event_id: str = "", owner: str = "legacy") -> dict:
    """Compatibility entry point; explicit IDs distinguish attempts, old retries deduplicate."""
    try:
        meta, _, errors = parse_card(task_file.read_text(encoding="utf-8"))
        if errors:
            raise ValueError("; ".join(errors))
        identity = event_id or "legacy:"+meta.get("head_sha", "")+":"+error_summary
        result = record_event(task_file, "fix", identity, owner, reason=error_summary)
        if result.get("error") or not result.get("is_fused"):
            return result
        # git-path works in a linked worktree, where .git is a file.
        raw = _checked_git(["rev-parse", "--git-path", "iter_consiliums"], repo_dir).strip()
        bundle_dir = Path(raw)
        if not bundle_dir.is_absolute():
            bundle_dir = repo_dir / bundle_dir
        bundle_dir.mkdir(parents=True, exist_ok=True)
        bundle = bundle_dir / ("consilium_"+task_file.stem+".md")
        template = (Path(__file__).resolve().parents[1]/"templates/consilium_rca_prompt.md").read_text(encoding="utf-8")
        for key, value in {
            "{task_file_path}": str(task_file.resolve()), "{iteration_name}": task_file.parent.name,
            "{base_sha}":meta.get("base_sha", ""), "{head_sha}":meta.get("head_sha", ""),
            "{files_changed_list}":"\n".join(extract_section_4_whitelist(task_file)),
            "{error_stack_summary}":error_summary or result["blocked_reason"]
        }.items():
            template = template.replace(key, value)
        if not bundle.exists() or bundle.read_text(encoding="utf-8") != template:
            bundle.write_text(template, encoding="utf-8")
        return {**result, "consilium_bundle":str(bundle.resolve())}
    except (OSError, ValueError, RuntimeError) as error:
        return {"error":str(error), "is_fused":True, "status":"BLOCKED"}



def verify_todos_committed(repo_dir: Path) -> dict:
    cwd = repo_dir.resolve()
    if cwd.is_file():
        cwd = cwd.parent
    result = _run_git(["status", "--porcelain", "-uall", "--ignored", "--", "docs/todos", ".gitignore"], cwd)
    if result.returncode:
        return {"committed": False, "dirty_files": [], "error": result.stderr.strip() or "git status failed"}
    dirty = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return {"committed": not dirty, "dirty_files": dirty}


def find_todos_root(start_dir: Path) -> Path:
    curr = start_dir.resolve()
    if curr.is_file():
        curr = curr.parent
    for _ in range(6):
        if curr.name == "todos" and curr.parent.name == "docs" and (curr / "README.md").exists():
            return curr
        candidate = curr / "docs" / "todos"
        if candidate.is_dir() and (candidate / "README.md").exists():
            return candidate
        if curr.parent == curr:
            break
        curr = curr.parent
    raise FileNotFoundError("Could not locate 'docs/todos/' directory upwards from current path.")


def is_feature_or_worktree(repo_dir: Path) -> tuple:
    cwd = repo_dir.resolve()
    if cwd.is_file():
        cwd = cwd.parent

    git_check = _run_git(["rev-parse", "--is-inside-work-tree"], cwd)
    if git_check.returncode != 0:
        return False, "Not inside a Git repository"

    branch_res = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd)
    branch = branch_res.stdout.strip() if branch_res.returncode == 0 else ""

    git_dir_res = _run_git(["rev-parse", "--git-dir"], cwd)
    git_dir = git_dir_res.stdout.strip() if git_dir_res.returncode == 0 else ""

    if ".worktrees" in cwd.as_posix() or ".worktrees" in git_dir:
        return True, f"Inside linked worktree: branch '{branch}' (git-dir: {git_dir})"

    if branch and branch not in ("main", "master"):
        return True, f"On non-main branch: '{branch}'"

    return False, f"On main branch: '{branch}'"



def resolve_target_iteration_dir(target_p: Path) -> Path:
    """Resolves iteration directory either from direct path or by scanning docs/todos/."""
    p = target_p.resolve()
    if p.is_file() or p.suffix:
        p = p.parent
    if p.is_dir() and any(f.name != "README.md" and f.suffix == ".md" for f in p.glob("*.md")):
        return p
    todos_d = find_todos_root(p)
    return resolve_local_iter_dir(p, todos_d)

def resolve_local_iter_dir(start_path: Path, todos_root: Path) -> Path:
    curr = start_path.resolve()
    if curr.is_file():
        curr = curr.parent

    if curr.parent == todos_root and (curr / "README.md").exists():
        return curr

    m = re.search(r"iter-(\d+)", curr.as_posix())
    if m:
        prefix = m.group(1).zfill(2)
        for d in todos_root.iterdir():
            if d.is_dir() and d.name.startswith(f"{prefix}-"):
                return d

    res = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], curr)
    if res.returncode == 0:
        branch = res.stdout.strip()
        m2 = re.search(r"iter-(\d+)", branch)
        if m2:
            prefix = m2.group(1).zfill(2)
            for d in todos_root.iterdir():
                if d.is_dir() and d.name.startswith(f"{prefix}-"):
                    return d

    # Filter valid iteration directories matching r"^\d+-" containing README.md (ignoring non-iteration folders like 'old', 'templates', 'archived')
    iter_subdirs = [
        d for d in todos_root.iterdir()
        if d.is_dir() and re.match(r"^\d+-", d.name) and (d / "README.md").exists()
    ]
    if len(iter_subdirs) == 1:
        return iter_subdirs[0]
    elif len(iter_subdirs) > 1:
        # If multiple active iterations exist on main, pick the first or prompt clearly
        pass

    raise ValueError(
        f"Cannot determine local iteration directory for '{start_path}'.\n"
        f"Please provide the iteration directory explicitly, e.g.:\n"
        f"  python iter_sync.py --local docs/todos/01-iteration-name"
    )


def update_table_row(content, links, updates):
    """Update linked index rows; support the bounded legacy Task/Status form."""
    headers, result = [], []
    for line in content.splitlines(keepends=True):
        if line.lstrip().startswith("|"):
            cells = line.strip().strip("|").split("|")
            labels = [cell.strip() for cell in cells]
            if (any(label in ("详细卡片索引", "迭代目录链接") for label in labels)
                    or {"Task", "Status"}.issubset(labels)):
                headers = ["状态" if label == "Status" else label for label in labels]
            elif headers and len(cells) == len(headers) and any(f"]({link})" in line for link in links):
                for label, value in updates.items():
                    if label in headers:
                        cells[headers.index(label)] = " " + value + " "
                line = "|" + "|".join(cells) + "|" + ("\n" if line.endswith("\n") else "")
        else:
            headers = []
        result.append(line)
    return "".join(result)


def markdown_text(value):
    import html
    return html.escape(str(value)).replace('|', '&#124;').replace('\n', ' ').replace('\r', '')


def replace_projection(content, text):
    block = '<!-- iter:projection -->\n'+text+'\n<!-- /iter:projection -->'
    if '<!-- iter:projection -->' in content:
        return re.sub(r'<!-- iter:projection -->.*?<!-- /iter:projection -->', lambda _:block, content, flags=re.S)
    return content.rstrip()+'\n\n'+block+'\n'


def projection_markdown(data):
    rows = ['## 验收事实（阶段比例不是工时）', '',
            f"声明DONE {data['done']}/{data['total']} · 验收PASS {data['accepted']}/{data['total']}", '',
            '| 任务 | 声明 | 验收 | 业务阶段 / 清单比例 | 工程阶段 | 阻塞原因 | 累计尝试 | 最后更新 |',
            '| --- | --- | --- | --- | --- | --- | --- | --- |']
    for c in data['cards']:
        values = [c['filename'],c['status'],c['acceptance_verdict'],c['stage_current']+' / '+c['stage_progress'],
                  c['tdd_step'],c['blocked_reason'] or '未记录',c['fix_total'],c['updated_at']]
        rows.append('| '+' | '.join(map(markdown_text,values))+' |')
    return '\n'.join(rows)


def sync_local_iteration(iter_dir: Path, dry_run: bool = False, strict: bool = False) -> dict:
    readme_path = iter_dir / "README.md"
    content = readme_path.read_text(encoding="utf-8")
    data = generate_board_data(iter_dir)
    try:
        _fs_root = load_profile(iter_dir)
        if _fs_root is not None:
            violations = []
        else:
            violations = committed_candidate_errors(iter_dir) if strict else []
    except ValueError as _pe:
        violations = [f"Profile error: {_pe}"]
    for card in data["cards"]:
        if card["status"] in ("DONE", "FUSED", "UNKNOWN") and card["acceptance_verdict"] != "PASS":
            violations.append(card["filename"]+": "+"; ".join(card["findings"] or [card["blocked_reason"] or card["acceptance_verdict"]]))
        badge = STATUS_BADGE_MAP.get(card["status"], "UNKNOWN")
        content = update_table_row(content, ("./"+card["filename"],card["filename"]),
                                   {"状态":badge+" / 验收:"+card["acceptance_verdict"]})
    content = re.sub(r"> \*\*进度指示\*\*：[^\n]*",
                     f"> **进度指示**：声明DONE [{data['done']}/{data['total']}] ({data['percentage']:g}%) · 验收PASS [{data['accepted']}/{data['total']}] · 状态：{data['status']}", content)
    content = replace_projection(content, projection_markdown(data))
    if not dry_run:
        readme_path.write_text(content, encoding="utf-8")
    return {**data, "gate_violations":violations}



def generate_review_package(base_sha: str, head_sha: str, task_id: str = "", repo_dir: Path = None) -> Path:
    cwd = (repo_dir if repo_dir else Path.cwd()).resolve()
    base = resolve_commit(base_sha, cwd)
    head = resolve_commit(head_sha, cwd)
    stat = _checked_git(["diff", "--stat", base, head, "--"], cwd)
    patch = _checked_git(["diff", "-p", "--no-color", "--no-ext-diff", base, head, "--"], cwd)
    log = _checked_git(["log", "--format=%H %s", base + ".." + head, "--"], cwd)
    git_path = _checked_git(["rev-parse", "--git-path", "iter_reviews"], cwd).strip()
    reviews_dir = Path(git_path)
    if not reviews_dir.is_absolute():
        reviews_dir = cwd / reviews_dir
    reviews_dir.mkdir(parents=True, exist_ok=True)
    safe_id = re.sub(r"[^A-Za-z0-9_.-]", "_", task_id)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    pkg = reviews_dir / f"review_{safe_id}_{base[:7]}_{head[:7]}_{stamp}.md"
    body = (f"# SDD Review Package\n\nTask: {task_id}\nBASE_SHA: {base}\nHEAD_SHA: {head}\n"
            f"\n## Commits\n{log}\n## Diff Stat\n{stat}\n## Full Diff\n```diff\n{patch}\n```\n")
    pkg.write_text(body, encoding="utf-8")
    return pkg


def check_branch_isolation(repo_dir: Path, base_branch: str = "main", strict: bool = False) -> dict:
    violations, changed, expected_prefix = [], [], None
    try:
        root = Path(_checked_git(["rev-parse", "--show-toplevel"], repo_dir).strip()).resolve()
        base = resolve_commit(base_branch, root)
        merge_base = _checked_git(["merge-base", base, "HEAD"], root).strip()
        committed = [p for p in _checked_git(["diff", "--no-renames", "--name-only", "-z", merge_base, "HEAD", "--"], root).split("\0") if p]
        dirty = worktree_changed_files(root)
        changed = sorted(set(committed) | set(dirty))
        branch = _checked_git(["rev-parse", "--abbrev-ref", "HEAD"], root).strip()
        match = re.search(r"iter-(\d+)", branch)
        expected_prefix = match.group(1).zfill(2) if match else None
        if "docs/todos/README.md" in changed:
            violations.append("Zero-Root-Touch violation: docs/todos/README.md modified")
        if expected_prefix:
            for path in changed:
                parts = path.split("/")
                if len(parts) >= 3 and parts[:2] == ["docs", "todos"] and not parts[2].startswith(expected_prefix + "-"):
                    violations.append(f"Other iteration modified: {path}")
        if strict:
            if dirty:
                violations.append("Uncommitted candidate changes: " + ", ".join(dirty))
            directories = [d for d in (root / "docs/todos").glob("[0-9]*-*") if d.is_dir()
                           and (not expected_prefix or d.name.startswith(expected_prefix + "-"))]
            if len(directories) != 1:
                violations.append("UNKNOWN: strict check requires exactly one target iteration")
            else:
                if os.path.lexists(directories[0] / "iteration-delivery.json"):
                    violations.append(f"{directories[0].name}: filesystem delivery is local-only; branch strict requires Git receipts")
                cards = discover_task_files(directories[0])
                if not cards:
                    violations.append("UNKNOWN: no task cards")
                covered = [(directories[0] / "README.md").relative_to(root).as_posix()]
                for card in cards:
                    audit = audit_task_file(card)
                    if not audit["is_valid_done"]:
                        violations.extend(f"{card.name}: {audit['verdict']}: {v}" for v in (audit["violations"] or ["Task is not DONE"]))
                    else:
                        covered += scope_paths(card.read_text(encoding="utf-8"))[0]
                        covered.append(card.relative_to(root).as_posix())
                for path in committed:
                    if not matches_scope(path, covered):
                        violations.append(f"Changed file not covered by valid DONE receipt: {path}")
    except (OSError, UnicodeError, ValueError, RuntimeError) as error:
        violations.append(str(error))
    return {"passed": not violations, "violations": violations,
            "expected_iter_prefix": expected_prefix, "total_changed_files": len(changed)}


def sync_todos(todos_root: Path, dry_run: bool = False, strict: bool = False) -> dict:
    root_readme = todos_root / "README.md"
    content = root_readme.read_text(encoding="utf-8")
    stats, active, violations = [], [], committed_candidate_errors(todos_root) if strict else []
    for directory in sorted(todos_root.iterdir()):
        match = re.match(r"^(\d+)-", directory.name)
        if not directory.is_dir() or not match:
            continue
        if strict and os.path.lexists(directory / "iteration-delivery.json"):
            violations.append(f"{directory.name}: filesystem delivery is local-only; global strict requires Git receipts")
        data = generate_board_data(directory)
        for card in data["cards"]:
            if card["status"] in ("DONE","FUSED","UNKNOWN") and card["acceptance_verdict"]!="PASS":
                violations.append(directory.name+"/"+card["filename"]+": "+"; ".join(card["findings"] or [card["blocked_reason"] or card["acceptance_verdict"]]))
        if data["in_progress"] or data["testing"]:
            active.append(directory.name)
        item = dict(num=match[1],dir_name=directory.name,total=data["total"],done=data["done"],
                    accepted=data["accepted"],pct=data["percentage"],status=data["status"],conclusion=data["conclusion"])
        stats.append(item)
        content = update_table_row(content, ("./"+directory.name+"/README.md",directory.name+"/README.md"),
                                   {"子任务数":str(item["total"]), "验收状态":item["status"]})
    total, done, accepted = (sum(s[key] for s in stats) for key in ("total","done","accepted"))
    pct = round(done/total*100,1) if total else 0
    if not total:
        status="暂无任务"
    elif any(s["conclusion"]=="BLOCKED" for s in stats):
        status="🔴 验收阻塞"
    elif any(s["conclusion"]=="FAIL" for s in stats):
        status="🔴 验收失败"
    elif accepted==total:
        status="🟢 验收通过"
    elif any(s["conclusion"]=="UNKNOWN" for s in stats):
        status="🟠 验收未知"
    elif active or done:
        status="🟡 进行中"
    else:
        status="⚪ 待开始"
    active_text = "["+", ".join(active)+"]" if active else "无活跃迭代"
    content = re.sub(r"当前活跃迭代：[^\n]*",
                     f"当前活跃迭代：`{active_text}` · 声明DONE占比：`{done}/{total} ({pct:g}%)` · 验收PASS：`{accepted}/{total}` · 状态：`{status}`",content)
    rows = ["## 验收事实（状态声明不等于批准）","",f"声明DONE {done}/{total} · 验收PASS {accepted}/{total}","",
            "| 迭代 | 声明DONE | 验收PASS | 验收结论 |","| --- | --- | --- | --- |"]
    for item in stats:
        rows.append(f"| {markdown_text(item['dir_name'])} | {item['done']}/{item['total']} | {item['accepted']}/{item['total']} | {item['conclusion']} |")
    content = replace_projection(content,"\n".join(rows))
    if not dry_run:
        root_readme.write_text(content,encoding="utf-8")
    return dict(total_tasks=total,total_done=done,total_accepted=accepted,percentage=pct,
                active_iters=active,iterations=stats,gate_violations=violations)






def disp_width(s: str) -> int:
    """Calculates visible terminal width accounting for East Asian full-width characters."""
    import unicodedata
    clean_s = re.sub(r'\x1b\[[0-9;]*m', '', s)
    w = 0
    for ch in clean_s:
        if unicodedata.east_asian_width(ch) in ('F', 'W'):
            w += 2
        else:
            w += 1
    return w


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




def _evidence_root(iter_dir: Path) -> Path | None:
    from iter_filesystem import load_profile
    try:
        prof_root = load_profile(iter_dir)
        if prof_root is not None:
            return prof_root
    except ValueError:
        return None
    try:
        return Path(_checked_git(["rev-parse", "--show-toplevel"], iter_dir).strip()).resolve()
    except RuntimeError:
        return iter_dir.resolve()


def generate_board_data(iter_dir: Path) -> dict:
    """Shared read-only projection for HTML, terminal and README."""
    cards = []
    root = _evidence_root(iter_dir)
    for tf in discover_task_files(iter_dir):
        try:
            text = tf.read_text(encoding="utf-8")
            meta, _, errors = parse_card(text)
        except (OSError, UnicodeError) as error:
            text, meta, errors = "", {}, [str(error)]
        st = card_status(text)
        micro = parse_task_stages_and_micro_state(text, st)
        audit = audit_task_file(tf)
        sources = []
        receipt = None
        try:
            if root is None:
                raise ValueError("Filesystem delivery profile invalid")
            receipt_file = contained(root, meta.get("review_receipt", ""))
            sources.append(dict(label="审查收据", path=receipt_file.relative_to(root).as_posix()))
            receipt = json.loads(receipt_file.read_text(encoding="utf-8"))
            values = [("独立审查报告", receipt.get("review_report"))]
            values += [(str(c.get("name","check"))+" 原始输出", c.get("output")) for c in receipt.get("checks",[]) if isinstance(c,dict)]
            for label, value in values:
                artifact = contained(root, value)
                sources.append(dict(label=label, path=artifact.relative_to(root).as_posix()))
        except (OSError, ValueError, TypeError, AttributeError):
            pass
        verdict = audit["verdict"]
        if errors or micro["errors"]:
            verdict = "FAIL"
        elif micro["is_blocked"]:
            verdict = "BLOCKED"
        scopes, _ = scope_paths(text)
        cards.append(dict(id=meta.get("task_id",tf.stem), name=meta.get("task_name",tf.stem),
                          filename=tf.name, status=st, type=meta.get("type","UNKNOWN"),
                          head_sha=meta.get("head_sha",""), base_sha=meta.get("base_sha",""),
                          review_status=meta.get("review_status","PENDING"),
                          acceptance_verdict=verdict, findings=errors+audit["violations"]+micro["errors"],
                          whitelist=scopes, sources=sources, updated_at=meta.get("updated_at","UNKNOWN"),
                          **{k:v for k,v in micro.items() if k!="errors"}))
    total = len(cards)
    counts = {key:sum(c["status"]==key for c in cards) for key in ("DONE","TODO","IN_PROGRESS","TESTING","FUSED","UNKNOWN")}
    accepted = sum(c["acceptance_verdict"]=="PASS" for c in cards)
    blocked = sum(c["acceptance_verdict"]=="BLOCKED" for c in cards)
    unknown = sum(c["acceptance_verdict"]=="UNKNOWN" for c in cards)
    failed = sum(c["acceptance_verdict"]=="FAIL" for c in cards)
    if not total:
        conclusion, badge = "EMPTY", "暂无任务"
    elif blocked:
        conclusion, badge = "BLOCKED", "🔴 验收阻塞"
    elif failed:
        conclusion, badge = "FAIL", "🔴 验收失败"
    elif accepted==total:
        conclusion, badge = "PASS", "🟢 验收通过"
    elif any(c["status"] in ("DONE","UNKNOWN") and c["acceptance_verdict"]!="PASS" for c in cards):
        conclusion, badge = "UNKNOWN", "🟠 验收未知"
    elif counts["IN_PROGRESS"] or counts["TESTING"] or counts["DONE"]:
        conclusion, badge = "PENDING", "🟡 进行中"
    else:
        conclusion, badge = "PENDING", "⚪ 待开始"
    return dict(iteration_name=iter_dir.name, total=total, done=counts["DONE"], accepted=accepted,
                percentage=round(counts["DONE"]/total*100,1) if total else 0,
                accepted_percentage=round(accepted/total*100,1) if total else 0,
                in_progress=counts["IN_PROGRESS"], testing=counts["TESTING"], fused=counts["FUSED"],
                todo=counts["TODO"], unknown=unknown, invalid_status=counts["UNKNOWN"],
                blocked=blocked, failed=failed, conclusion=conclusion, status=badge,
                generated_at=datetime.now().astimezone().isoformat(), cards=cards)



def build_html_dashboard(data: dict) -> str:
    """Embed inert JSON; the static template uses text nodes, not HTML sinks."""
    encoded = json.dumps(data, ensure_ascii=False)
    for char, escaped in (("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026"),
                          ("\u2028", "\\u2028"), ("\u2029", "\\u2029")):
        encoded = encoded.replace(char, escaped)
    template = Path(__file__).resolve().parents[1] / "templates" / "board.html"
    return template.read_text(encoding="utf-8").replace("__ITER_BOARD_DATA__", encoded)




class LiveBoardHandler(http.server.BaseHTTPRequestHandler):
    iter_dir = None

    def do_GET(self):
        from urllib.parse import urlsplit, parse_qs
        port = self.server.server_address[1]
        hosts = {f'127.0.0.1:{port}', f'localhost:{port}'}
        origin = self.headers.get('Origin')
        if self.headers.get('Host') not in hosts or (origin and origin not in {'http://'+h for h in hosts}):
            self.send_error(403, 'Local same-origin requests only')
            return
        route = urlsplit(self.path)
        try:
            data = generate_board_data(self.iter_dir)
            if route.path == '/api/board':
                body = json.dumps(data,ensure_ascii=False).encode('utf-8')
                mime = 'application/json; charset=utf-8'
            elif route.path == '/':
                body = build_html_dashboard(data).encode('utf-8')
                mime = 'text/html; charset=utf-8'
            elif route.path == '/api/evidence':
                query = parse_qs(route.query)
                name = query.get('task',[''])[0]
                card = next(c for c in data['cards'] if c['filename']==name)
                raw_index = query.get('source',[''])[0]
                if not raw_index.isdigit():
                    raise ValueError('Invalid source index')
                source = card['sources'][int(raw_index)]
                root = _evidence_root(self.iter_dir)
                if root is None:
                    raise ValueError('Filesystem delivery profile invalid')
                path = contained(root,source['path'])
                body = path.read_bytes()
                mime = {'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp'}.get(path.suffix.lower(),'text/plain; charset=utf-8')
            else:
                self.send_error(404)
                return
        except (OSError,ValueError,IndexError,KeyError,StopIteration):
            self.send_error(404,'Evidence or task not found')
            return
        self.send_response(200)
        self.send_header('Content-Type',mime)
        self.send_header('Content-Length',str(len(body)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('X-Frame-Options','DENY')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Silence standard HTTP access logging to keep console clean
        pass


def serve_live_board(iter_dir: Path, port: int = 8765, open_browser: bool = True):
    handler = type('IterationBoardHandler',(LiveBoardHandler,),dict(iter_dir=iter_dir))
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1',port),handler)
    url = f"http://127.0.0.1:{httpd.server_address[1]}"
    print(f"\n[IterSync:LiveBoard] HTML Board Server listening on: {url}")
    print(f"   -> Real-time 2s auto-refresh active. Press Ctrl+C to stop.\n")

    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[IterSync:LiveBoard] Server stopped.")
    finally:
        httpd.server_close()


def render_terminal_board(iter_dir: Path, stream=None):
    """Use the same facts as HTML. No implicit APPROVED, test pass or stage estimate."""
    if stream is None:
        stream = sys.stdout
    data = generate_board_data(iter_dir)
    lines = [f"Iteration Board: {data['iteration_name']} | {data['conclusion']}",
             f"声明DONE: {data['done']}/{data['total']} | 验收PASS: {data['accepted']}/{data['total']}"]
    if not data["cards"]:
        lines.append("暂无任务；验收未开始")
    for card in data["cards"]:
        lines += [f"[{card['status']}] {card['id']}. {card['name']} | 验收:{card['acceptance_verdict']}",
                  f"  业务阶段: {card['stage_current']} | 清单完成比例: {card['stage_progress']} (非工时)",
                  f"  工程阶段: {card['tdd_step']} | 修复轮次/累计: {card['fix_rounds']}/{card['fix_total']} | 重规划:{card['replan_count']}",
                  f"  阻塞: {card['blocked_reason'] or '未记录'} | 更新时间: {card['updated_at']}"]
        for source in card["sources"]:
            lines.append(f"  证据 {source['label']}: {source['path']}")
    stream.write("\n".join(lines)+"\n")
    stream.flush()




def main():
    start_time = time.perf_counter()
    args = sys.argv[1:]
    if args and args[0] == '--timing-init':
        from iter_timing import initialize
        if len(args) != 3:
            raise ValueError('Usage: --timing-init <trace> <session-id>')
        initialize(Path.cwd(), args[1], args[2])
        return
    if args and args[0] == '--timing-import':
        from iter_timing import import_record
        if len(args) != 3:
            raise ValueError('Usage: --timing-import <trace> <observation-json>')
        import_record(Path.cwd(), args[1], args[2])
        return
    if args and args[0] == '--timing-import-receipt':
        import argparse
        from iter_timing import import_receipt, CATEGORIES
        parser = argparse.ArgumentParser()
        parser.add_argument('trace')
        parser.add_argument('receipt')
        parser.add_argument('--category', choices=sorted(CATEGORIES), required=True)
        parser.add_argument('--operation', required=True)
        parser.add_argument('--target', required=True)
        opt = parser.parse_args(args[1:])
        import_receipt(Path.cwd(), opt.trace, opt.receipt, opt.category, opt.operation, opt.target)
        return
    if args and args[0] == '--timing-report':
        from iter_timing import report
        if len(args) != 2:
            raise ValueError('Usage: --timing-report <trace>')
        result = report(Path.cwd(), args[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result['errors']:
            sys.exit(2)
        return
    if args and args[0] == '--inventory':
        import argparse
        from iter_inventory import inventory
        parser = argparse.ArgumentParser()
        parser.add_argument('target', type=Path)
        parser.add_argument('--mode', required=True, choices=('continue', 'takeover'))
        parser.add_argument('--context')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--phase', default='implementation')
        group.add_argument('--phase-from-context', action='store_true')
        parser.add_argument('--details', action='store_true')
        parser.add_argument('--timing-trace')
        opt = parser.parse_args(args[1:])
        if opt.timing_trace:
            from iter_timing import append, now
            from uuid import uuid4
            timing_id = str(uuid4())
            append(Path.cwd(), opt.timing_trace, dict(type='start', id=timing_id,
                   category='inventory', operation='inventory', target=str(opt.target),
                   requested_phase='context' if opt.phase_from_context else opt.phase,
                   mode=opt.mode, context=opt.context, details=opt.details,
                   started_at=now(), clock_basis='local_utc', source_kind='instrumented', source='trace'))
        phase_details = [] if opt.timing_trace else None
        result = inventory(opt.target, Path.cwd(), opt.mode, opt.context, opt.phase, opt.phase_from_context, opt.details, phase_details) if opt.timing_trace else inventory(opt.target, Path.cwd(), opt.mode, opt.context, opt.phase, opt.phase_from_context, opt.details)
        if opt.timing_trace:
            append(Path.cwd(), opt.timing_trace, dict(type='finish', id=timing_id, ended_at=now(),
                   outcome=result['readiness'], observed_phases=[task.get('phase') for task in result.get('tasks', [])],
                   phase_details=phase_details))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result['readiness'] != 'READY':
            sys.exit(3 if result['readiness'] == 'BLOCKED' else 2)
        return
    if args and args[0] == '--execution-report':
        from iter_execution import execution_report
        if len(args) != 2:
            raise ValueError('Usage: --execution-report <iteration-directory>')
        result = execution_report(Path(args[1]), Path.cwd())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result['errors']:
            sys.exit(2)
        return
    if args and args[0] in ('--preflight', '--dispatch-check'):
        import argparse
        from iter_preflight import preflight, preflight_from_context, dispatch_check
        parser = argparse.ArgumentParser()
        parser.add_argument('target', type=Path)
        parser.add_argument('--context')
        phase_group = parser.add_mutually_exclusive_group()
        phase_group.add_argument('--phase', default='implementation')
        phase_group.add_argument('--phase-from-context', action='store_true')
        parser.add_argument('--owner', default='')
        parser.add_argument('--timing-trace')
        opt = parser.parse_args(args[1:])
        if opt.phase_from_context and args[0] != '--preflight':
            parser.error('--phase-from-context applies only to --preflight')
        if opt.timing_trace and args[0] != '--preflight':
            parser.error('--timing-trace applies only to --preflight')
        if opt.timing_trace:
            from iter_timing import append, now
            from uuid import uuid4
            timing_id = str(uuid4())
            append(Path.cwd(), opt.timing_trace, dict(type='start', id=timing_id,
                   category='inventory', operation='preflight', target=str(opt.target),
                   requested_phase='context' if opt.phase_from_context else opt.phase,
                   context=opt.context, owner=opt.owner,
                   started_at=now(), clock_basis='local_utc', source_kind='instrumented', source='trace'))
        check = preflight if args[0] == '--preflight' else dispatch_check
        phase_details = [] if opt.timing_trace else None
        if opt.timing_trace:
            from iter_preflight import _preflight
            result = _preflight(opt.target, Path.cwd(), opt.context, opt.phase, opt.owner, audit_task_file, opt.phase_from_context, phase_details)
        elif opt.phase_from_context:
            result = preflight_from_context(opt.target, Path.cwd(), opt.context, opt.owner, audit_task_file)
        else:
            result = check(opt.target, Path.cwd(), opt.context, opt.phase, opt.owner, audit_task_file)
        if opt.timing_trace:
            append(Path.cwd(), opt.timing_trace, dict(type='finish', id=timing_id, ended_at=now(),
                   outcome=result['readiness'], observed_phases=[task.get('phase') for task in result.get('tasks', [])],
                   phase_details=phase_details))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result['readiness'] != 'READY':
            sys.exit(3 if result['readiness'] == 'BLOCKED' else 2)
        return
    if args in (['--help'], ['-h']):
        print('Iteration Manager: --verify-committed | --takeover-report <iteration-dir> | --inventory <iteration-dir> --mode {continue,takeover} [--context JSON (--phase PHASE | --phase-from-context) --details] | --execution-report <iteration-dir> | --preflight <iteration-dir> [--context JSON (--phase PHASE | --phase-from-context) --owner OWNER] | --dispatch-check <card> [--context JSON --phase PHASE --owner OWNER] | --render-envelope <card> [repo] | --autonomy <action including attempt> <card> --event-id ID --owner OWNER | --check-scope BASE HEAD CARD [--include-worktree] | --review-pkg BASE HEAD [task] [repo] | --local [--strict] [path] | --check-branch [--strict] [repo] [base] | --board | --serve-board [port] [path] | --export-board [path]. See references/execution_readiness.md for opt-in readiness/attempt reports; references/agent_protocol.md for recovery and budgets.')
        return
    if args and args[0] == '--takeover-report':
        if len(args) != 2:
            raise ValueError('Usage: --takeover-report <iteration-directory>')
        directory = Path(args[1])
        if not directory.is_dir():
            raise ValueError('Iteration directory not found')
        tasks = []
        for path in discover_task_files(directory):
            meta, _, errors = parse_card(path.read_text(encoding='utf-8'))
            audit = audit_task_file(path)
            tasks.append(dict(path=str(path), declared_status=audit['status'], acceptance_verdict=audit['verdict'],
                              missing=[k for k in ('schema_version','type','task_id','review_receipt') if not meta.get(k)],
                              findings=errors+audit['violations']))
        print(json.dumps(dict(read_only=True, tasks=tasks, next='Request migration/reverification authorization; preserve history'), ensure_ascii=False))
        return
    if args and args[0] == '--autonomy':
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('action', choices=['claim','fix','consilium','replan','recover','release','closeout','resume-checkpoint','attempt'])
        parser.add_argument('task_file', type=Path)
        parser.add_argument('--event-id', required=True)
        parser.add_argument('--owner', required=True)
        parser.add_argument('--reason', default='')
        parser.add_argument('--evidence', default='')
        parser.add_argument('--executor-state', default='')
        parser.add_argument('--resume-grant')
        opt = parser.parse_args(args[1:])
        result = record_event(opt.task_file, opt.action, opt.event_id, opt.owner, opt.reason, opt.evidence, opt.executor_state, opt.resume_grant)
        print(json.dumps(result, ensure_ascii=False))
        if result.get('error'):
            sys.exit(2)
        if result.get('is_fused'):
            sys.exit(3)
        return
    known_flags = {'--dry-run','--strict','--force-root','--local','--check-branch','--review-pkg',
                   '--verify-committed','--check-scope','--render-envelope','--record-fix','--board',
                   '--serve-board','--export-board','--include-worktree','--baseline-dirty'}
    if any(a.startswith('--') and a not in known_flags for a in args):
        raise ValueError('Unknown option; no synchronization performed')
    baseline_dirty = None
    if "--baseline-dirty" in args:
        index = args.index("--baseline-dirty")
        if index + 1 >= len(args):
            raise ValueError("--baseline-dirty requires a JSON file")
        baseline_dirty = json.loads(Path(args[index + 1]).read_text(encoding="utf-8"))
        del args[index:index + 2]
    include_worktree = "--include-worktree" in args
    dry_run = "--dry-run" in args
    strict = "--strict" in args
    force_root = "--force-root" in args
    is_local = "--local" in args
    is_check_branch = "--check-branch" in args
    is_review_pkg = "--review-pkg" in args
    is_verify_committed = "--verify-committed" in args
    is_check_scope = "--check-scope" in args
    is_render_envelope = "--render-envelope" in args
    is_record_fix = "--record-fix" in args
    is_board = "--board" in args
    is_serve_board = "--serve-board" in args
    is_export_board = "--export-board" in args

    clean_args = [
        a for a in args if a not in (
            "--dry-run", "--strict", "--force-root", "--local",
            "--check-branch", "--review-pkg", "--verify-committed",
            "--check-scope", "--render-envelope", "--record-fix", "--board", "--serve-board", "--export-board", "--include-worktree"
        )
    ]

    target_path = Path(clean_args[0]) if clean_args else Path.cwd()

    # 1. [Scope Firewall] python iter_sync.py --check-scope <BASE_SHA> <HEAD_SHA> <task_file> [repo_dir]
    if is_check_scope:
        if len(clean_args) < 3:
            print("[IterSync:Error] Usage: python iter_sync.py --check-scope <BASE_SHA> <HEAD_SHA> <task_file> [repo_dir]", file=sys.stderr)
            sys.exit(1)
        base_sha, head_sha = clean_args[0], clean_args[1]
        task_f = Path(clean_args[2])
        repo_d = Path(clean_args[3]) if len(clean_args) >= 4 else Path.cwd()
        res = audit_scope_firewall(repo_d, base_sha, head_sha, task_f, include_worktree, baseline_dirty)
        if res.get("preexisting_files"):
            print("[IterSync:Ownership] Pre-existing changes require owner verification: " + ", ".join(res["preexisting_files"]), file=sys.stderr)
        if not res["passed"]:
            print("[IterSync:ScopeFirewall:FAILED] Out-of-scope files detected:", file=sys.stderr)
            for v in res["violations"]:
                print(f"  - {v}", file=sys.stderr)
            sys.exit(2)
        print(f"[IterSync:ScopeFirewall:PASSED] All {len(res['changed_files'])} changed files within declared scope; ownership is not inferred.")
        return

    # 2. [Task Handoff Envelope] python iter_sync.py --render-envelope <task_file> [repo_dir]
    if is_render_envelope:
        if len(clean_args) < 1:
            print("[IterSync:Error] Usage: python iter_sync.py --render-envelope <task_file> [repo_dir]", file=sys.stderr)
            sys.exit(1)
        task_f = Path(clean_args[0])
        repo_d = Path(clean_args[1]) if len(clean_args) >= 2 else Path.cwd()
        env = render_task_envelope(task_f, repo_d)
        print(json.dumps(env, ensure_ascii=False, indent=2))
        return

    # 3. [Circuit Breaker & Consilium] python iter_sync.py --record-fix <task_file> [error_summary] [repo_dir]
    if is_record_fix:
        if len(clean_args) < 1:
            print("[IterSync:Error] Usage: python iter_sync.py --record-fix <task_file> [error_summary] [repo_dir]", file=sys.stderr)
            sys.exit(1)
        task_f = Path(clean_args[0])
        err_sum = clean_args[1] if len(clean_args) >= 2 else ""
        repo_d = Path(clean_args[2]) if len(clean_args) >= 3 else Path.cwd()
        res = record_fix_and_check_fuse(task_f, repo_d, err_sum)
        if res.get('error'):
            print(json.dumps(res, ensure_ascii=False), file=sys.stderr)
            sys.exit(2)
        if res.get("is_fused"):
            print(f"[IterSync:CircuitBreaker:FUSED] Task reached 5 fix rounds! Circuit breaker tripped.")
            print(f"  -> Status flipped to: 🔴 已熔断 (FUSED)")
            print(f"  -> Consilium Bundle created: {res['consilium_bundle']}")
            sys.exit(3)
        else:
            print(f"[IterSync:CircuitBreaker:OK] Fix round recorded: {res['current_rounds']}/5 (Status: {res['status']})")
        return

    # 4. [Serve Live HTML Board] python iter_sync.py --serve-board [port] [iter_dir | repo_dir]
    if is_serve_board:
        try:
            port = 8765
            if clean_args and clean_args[0].isdigit():
                port = int(clean_args.pop(0))
            target_p = Path(clean_args[0]) if clean_args else Path.cwd()
            iter_d = resolve_target_iteration_dir(target_p)
            serve_live_board(iter_d, port=port, open_browser=True)
        except Exception as e:
            print(f"[IterSync:ServeBoardError] {e}", file=sys.stderr)
            sys.exit(1)
        return

    # 5. [Export Static HTML Board] python iter_sync.py --export-board [output_file] [iter_dir | repo_dir]
    if is_export_board:
        try:
            target_p = Path(clean_args[0]) if clean_args else Path.cwd()
            iter_d = resolve_target_iteration_dir(target_p)
            data = generate_board_data(iter_d)
            html_out = build_html_dashboard(data)
            out_path = iter_d / "board.html"
            out_path.write_text(html_out, encoding="utf-8")
            print(f"[IterSync:ExportBoard] Successfully exported standalone HTML board -> {out_path.resolve().as_posix()}")
        except Exception as e:
            print(f"[IterSync:ExportBoardError] {e}", file=sys.stderr)
            sys.exit(1)
        return

    # 6. [Terminal Rich Board] python iter_sync.py --board [iter_dir | repo_dir]
    if is_board:
        try:
            iter_d = resolve_target_iteration_dir(target_path)
            render_terminal_board(iter_d)
        except Exception as e:
            print(f"[IterSync:BoardError] {e}", file=sys.stderr)
            sys.exit(1)
        return

    # 5. Existing commands
    if is_review_pkg:
        if len(clean_args) < 2:
            print("[IterSync:Error] Usage: python iter_sync.py --review-pkg <BASE_SHA> <HEAD_SHA> [task_id] [repo_dir]", file=sys.stderr)
            sys.exit(1)
        base_sha = clean_args[0]
        head_sha = clean_args[1]
        task_id = clean_args[2] if len(clean_args) >= 3 else ""
        repo_dir = Path(clean_args[3]) if len(clean_args) >= 4 else Path.cwd()
        pkg = generate_review_package(base_sha, head_sha, task_id, repo_dir)
        print(f"[IterSync:ReviewPackage] Generated review diff package -> '{pkg.resolve().as_posix()}'")
        return

    if is_verify_committed:
        res = verify_todos_committed(target_path)
        if not res["committed"]:
            print("[IterSync:VerifyCommitted:FAILED] Uncommitted files detected in 'docs/todos/' or '.gitignore':", file=sys.stderr)
            if res.get("error"):
                print(res["error"], file=sys.stderr)
            for df in res["dirty_files"]:
                print(f"    {df}", file=sys.stderr)
            sys.exit(2)
        print("[IterSync:VerifyCommitted:PASSED] All 'docs/todos/' files are cleanly committed to Git.")
        return

    if is_check_branch:
        base_branch = clean_args[1] if len(clean_args) >= 2 else "main"
        res = check_branch_isolation(target_path, base_branch=base_branch, strict=strict)
        if not res["passed"]:
            print("[IterSync:CheckBranch:FAILED] Zero-Root-Touch or Strict Gate violations found:", file=sys.stderr)
            for v in res["violations"]:
                print(f"  - {v}", file=sys.stderr)
            sys.exit(2)
        print(f"[IterSync:CheckBranch:PASSED] Branch complies 100% with Zero-Root-Touch (scoped to iter-{res['expected_iter_prefix'] or 'auto'}).")
        return

    try:
        todos_dir = find_todos_root(target_path)
    except Exception as e:
        print(f"[IterSync:Error] {e}", file=sys.stderr)
        sys.exit(1)

    if is_local:
        try:
            iter_dir = resolve_local_iter_dir(target_path, todos_dir)
            res = sync_local_iteration(iter_dir, dry_run=dry_run, strict=strict)
        except Exception as e:
            print(f"[IterSync:LocalError] {e}", file=sys.stderr)
            sys.exit(1)
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        if res["gate_violations"]:
            for gv in res["gate_violations"]:
                print(f"[IterSync:AuditWarning] {gv}", file=sys.stderr)
        render_terminal_board(iter_dir)
        print(
            f"[IterSync:Local] Calibrated '{iter_dir.name}/README.md' -> "
            f"[{res['done']}/{res['total']}] ({res['percentage']}%) {res['status']} "
            f"in {elapsed_ms:.2f}ms (Zero-Root-Touch preserved)."
        )
        if strict and res["gate_violations"]:
            sys.exit(2)
        return

    isolated, reason = is_feature_or_worktree(target_path)
    if isolated and not force_root:
        print(
            f"[IterSync:Guard] Zero-Root-Touch active ({reason})! "
            f"Refusing to modify root 'docs/todos/README.md' inside a worktree/feature branch.\n"
            f"  -> To update current iteration's README locally, run: python iter_sync.py --local\n"
            f"  -> Run global '/iter sync' only on 'main' after merging the iteration branch.",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        result = sync_todos(todos_dir, dry_run=dry_run, strict=strict)
    except Exception as e:
        print(f"[IterSync:Error] {e}", file=sys.stderr)
        sys.exit(1)

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    if result.get("gate_violations"):
        for gv in result["gate_violations"]:
            print(f"[IterSync:AuditWarning] {gv}", file=sys.stderr)
    print(
        f"[IterSync] Scanned {len(result['iterations'])} iterations, "
        f"{result['total_tasks']} tasks ({result['total_done']} completed, {result['percentage']}%)."
    )
    print(f"[IterSync] Active iterations: {result['active_iters'] if result['active_iters'] else 'None'}")
    print(f"[IterSync] Successfully calibrated '{todos_dir / 'README.md'}' in {elapsed_ms:.2f}ms.")
    if strict and result["gate_violations"]:
        sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        print(f"[IterSync:Error] {error}", file=sys.stderr)
        sys.exit(1)
