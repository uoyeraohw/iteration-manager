#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit and Integration Tests for Multi-Worktree Concurrency, Directory-level Isolation,
SDD Review Package Generation, Four-State Gate Auditing, Local Iteration Sync,
and Pre-Worktree Serialization Commit Guard.
"""

import os
import sys
import shutil
import subprocess
import pytest
from pathlib import Path

# Add scripts directory to sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
from iter_sync import (
    sync_todos,
    scan_task_file,
    sync_local_iteration,
    audit_task_file,
    check_branch_isolation,
    generate_review_package,
    verify_todos_committed,
)

def run_cmd(args, cwd, check=True):
    res = subprocess.run(
        args,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=check
    )
    return res

@pytest.fixture
def git_repo_with_worktrees(tmp_path):
    """Creates a temporary git repository with two worktrees."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    
    # Configure git user
    run_cmd(["git", "init", "-b", "main"], repo_dir)
    run_cmd(["git", "config", "user.name", "Test Agent"], repo_dir)
    run_cmd(["git", "config", "user.email", "agent@test.local"], repo_dir)

    # Set up docs/todos directory structure
    todos_dir = repo_dir / "docs" / "todos"
    todos_dir.mkdir(parents=True)
    
    iter1_dir = todos_dir / "01-iter-one"
    iter1_dir.mkdir()
    iter1_readme = (
        "# 📌 迭代详情索引：01 - iter-one\n\n"
        "> **迭代定位**：`docs/todos/01-iter-one/`  \n"
        "> **进度指示**：`[0/1] (0%)` · 状态：`⚪ 待开始`  \n"
        "> **更新时间**：`2026-10-14 12:00` · **负责人**：Antigravity Agent\n\n"
        "## 🗂️ 子任务执行概况与目录索引 (Task Breakdown Index)\n\n"
        "| 任务序号 | 任务名称 | 核心目标概况 | 责任文件/主要改动 | 状态 | 详细卡片索引 |\n"
        "| :---: | :--- | :--- | :--- | :---: | :--- |\n"
        "| **01** | `01-task` | 测试任务 1 | `src/a.py` | ⚪ 待开始 | [01-task.md](./01-task.md) |\n"
    )
    (iter1_dir / "README.md").write_text(iter1_readme, encoding="utf-8")
    (iter1_dir / "01-task.md").write_text("---\nstatus: '⚪ 待开始 (TODO)'\n---\n# Task 01\n", encoding="utf-8")

    iter2_dir = todos_dir / "02-iter-two"
    iter2_dir.mkdir()
    (iter2_dir / "README.md").write_text("# Iter 02\n> **进度指示**：`[0/1] (0%)` · 状态：`⚪ 待开始`\n", encoding="utf-8")
    (iter2_dir / "01-task.md").write_text("---\nstatus: '⚪ 待开始 (TODO)'\n---\n# Task 02\n", encoding="utf-8")

    root_readme = (
        "# 📋 项目迭代总控管理索引 (Iteration Index)\n\n"
        "> **全局看板与多活并行指示**：当前活跃迭代：`无活跃迭代` · 整体进度：`0/2 (0%)` · 状态：`⚪ 待开始`  \n"
        "> **更新时间**：`2026-10-14 12:00` · **状态维护者**：Antigravity Agent (Iteration Manager / iter_sync)\n\n"
        "---\n\n"
        "## 🎯 整体项目阶段目标与路线图\n\n"
        "| 迭代序号 | 迭代名称 | 阶段核心目标 | 子任务数 | 验收状态 | 迭代目录链接 |\n"
        "| :---: | :--- | :--- | :---: | :---: | :--- |\n"
        "| **01** | `01-iter-one` | 阶段 1 目标 | 1 | ⚪ 待开始 | [01-iter-one](./01-iter-one/README.md) |\n"
        "| **02** | `02-iter-two` | 阶段 2 目标 | 1 | ⚪ 待开始 | [02-iter-two](./02-iter-two/README.md) |\n\n"
        "---\n"
    )
    (todos_dir / "README.md").write_text(root_readme, encoding="utf-8")

    # Initial commit on main
    run_cmd(["git", "add", "."], repo_dir)
    run_cmd(["git", "commit", "-m", "Initial commit with todos"], repo_dir)

    # Create two worktrees
    wt1_dir = tmp_path / "wt1"
    wt2_dir = tmp_path / "wt2"
    run_cmd(["git", "worktree", "add", "-b", "feat/iter-01", str(wt1_dir), "main"], repo_dir)
    run_cmd(["git", "worktree", "add", "-b", "feat/iter-02", str(wt2_dir), "main"], repo_dir)

    yield repo_dir, wt1_dir, wt2_dir

    # Teardown
    try:
        run_cmd(["git", "worktree", "remove", "--force", str(wt1_dir)], repo_dir, check=False)
        run_cmd(["git", "worktree", "remove", "--force", str(wt2_dir)], repo_dir, check=False)
    except Exception:
        pass

def test_directory_isolation_merge_zero_conflict(git_repo_with_worktrees):
    """
    Validates that when Worktrees follow directory-level isolation (only editing docs/todos/{iter}/*),
    Git merges with 100% ZERO conflict and /iter sync on main perfectly calibrates the global roadmap.
    """
    repo_dir, wt1_dir, wt2_dir = git_repo_with_worktrees

    # --- In Worktree 1 (feat/iter-01): Only touch 01-iter-one/ ---
    wt1_task = wt1_dir / "docs" / "todos" / "01-iter-one" / "01-task.md"
    wt1_task.write_text("---\nstatus: '🟢 已完成 (DONE)'\n---\n# Task 01\n", encoding="utf-8")

    wt1_iter_readme = wt1_dir / "docs" / "todos" / "01-iter-one" / "README.md"
    wt1_iter_readme.write_text("# Iter 01\n> **进度指示**：`[1/1] (100%)` · 状态：`🟢 已完成`\n", encoding="utf-8")

    run_cmd(["git", "add", "."], wt1_dir)
    run_cmd(["git", "commit", "-m", "Complete iter 01 task"], wt1_dir)

    # --- In Worktree 2 (feat/iter-02): Only touch 02-iter-two/ ---
    wt2_task = wt2_dir / "docs" / "todos" / "02-iter-two" / "01-task.md"
    wt2_task.write_text("---\nstatus: '🟡 进行中 (IN_PROGRESS)'\n---\n# Task 02\n", encoding="utf-8")

    wt2_iter_readme = wt2_dir / "docs" / "todos" / "02-iter-two" / "README.md"
    wt2_iter_readme.write_text("# Iter 02\n> **进度指示**：`[0/1] (0%)` · 状态：`🟡 进行中`\n", encoding="utf-8")

    run_cmd(["git", "add", "."], wt2_dir)
    run_cmd(["git", "commit", "-m", "Start iter 02 task"], wt2_dir)

    # --- Merge both into main ---
    merge_out1 = run_cmd(["git", "merge", "feat/iter-01", "--no-edit"], repo_dir).stdout
    assert "CONFLICT" not in merge_out1

    merge_out2 = run_cmd(["git", "merge", "feat/iter-02", "--no-edit"], repo_dir).stdout
    assert "CONFLICT" not in merge_out2

    status_out = run_cmd(["git", "status"], repo_dir).stdout
    assert "working tree clean" in status_out

    # --- Trigger /iter sync on main ---
    todos_dir = repo_dir / "docs" / "todos"
    sync_res = sync_todos(todos_dir)
    assert sync_res["total_tasks"] == 2
    assert sync_res["total_done"] == 1
    assert sync_res["percentage"] == 50
    assert sync_res["active_iters"] == ["02-iter-two"]

    calibrated_root = (todos_dir / "README.md").read_text(encoding="utf-8")
    assert "当前活跃迭代：`[02-iter-two]` · 声明DONE占比：`1/2 (50%)` · 验收PASS：`0/2` · 状态：`🟠 验收未知`" in calibrated_root
    assert "| **01** | `01-iter-one` | 阶段 1 目标 | 1 | 🟠 验收未知 |" in calibrated_root
    assert "| **02** | `02-iter-two` | 阶段 2 目标 | 1 个任务 | 🟡 进行中 |" in calibrated_root or "| **02** | `02-iter-two` | 阶段 2 目标 | 1 | 🟡 进行中 |" in calibrated_root

def test_local_iteration_sync_zero_root_touch(git_repo_with_worktrees):
    """Validates --local syncs only the target iteration's README.md and never touches root README.md."""
    _, wt1_dir, _ = git_repo_with_worktrees
    iter1_dir = wt1_dir / "docs" / "todos" / "01-iter-one"
    root_readme = wt1_dir / "docs" / "todos" / "README.md"
    before_root = root_readme.read_text(encoding="utf-8")

    # Update task 01 to DONE
    (iter1_dir / "01-task.md").write_text(
        "---\nstatus: '🟢 已完成 (DONE)'\ntdd_verified: true\nreview_status: 'APPROVED'\n---\n# Task 01\n",
        encoding="utf-8"
    )

    res = sync_local_iteration(iter1_dir)
    assert res["total"] == 1
    assert res["done"] == 1
    assert res["percentage"] == 100
    assert res["status"] == "🟠 验收未知"
    assert res["accepted"] == 0

    updated_iter_readme = (iter1_dir / "README.md").read_text(encoding="utf-8")
    assert "声明DONE [1/1] (100%)" in updated_iter_readme
    assert "验收PASS [0/1]" in updated_iter_readme
    assert "🟢 已完成" in updated_iter_readme
    # Root README must remain 100% untouched
    assert root_readme.read_text(encoding="utf-8") == before_root

def test_strict_gate_blocks_false_done_without_review_or_tdd(tmp_path):
    """Validates that a task marked DONE without Reviewer approval or TDD verification fails strict audit."""
    card = tmp_path / "01-false-done.md"
    card.write_text(
        "---\n"
        "status: '🟢 已完成 (DONE)'\n"
        "tdd_verified: false\n"
        "review_status: 'PENDING'\n"
        "---\n"
        "## 🛡️ 5. 确定性验收标准\n"
        "- [x] 单测通过\n"
        "- [ ] 边界检查未做\n",
        encoding="utf-8"
    )
    audit = audit_task_file(card)
    assert audit["status"] == "DONE"
    assert audit["is_valid_done"] is False
    assert len(audit["violations"]) >= 2

    # Legacy flags alone are not evidence; preserve declared DONE, require migration.
    card.write_text(
        "---\n"
        "status: '🟢 已完成 (DONE)'\n"
        "tdd_verified: true\n"
        "review_status: 'APPROVED'\n"
        "---\n"
        "## 🛡️ 5. 确定性验收标准\n"
        "- [x] 单测通过\n"
        "- [x] 边界检查完成\n",
        encoding="utf-8"
    )
    audit_ok = audit_task_file(card)
    assert audit_ok["is_valid_done"] is False
    assert audit_ok["verdict"] == "UNKNOWN"

def test_check_branch_detects_root_readme_violation(git_repo_with_worktrees):
    """Validates --check-branch catches forbidden edits to root docs/todos/README.md or foreign iterations."""
    _, wt1_dir, _ = git_repo_with_worktrees

    clean_check = check_branch_isolation(wt1_dir, base_branch="main")
    assert clean_check["passed"] is True

    root_readme = wt1_dir / "docs" / "todos" / "README.md"
    root_readme.write_text("# Illegally modified in branch\n", encoding="utf-8")

    dirty_check = check_branch_isolation(wt1_dir, base_branch="main")
    assert dirty_check["passed"] is False
    assert any("docs/todos/README.md" in v for v in dirty_check["violations"])

def test_generate_review_package_clean_worktree(git_repo_with_worktrees):
    """Validates --review-pkg generates a self-contained diff file inside .git without polluting git status."""
    _, wt1_dir, _ = git_repo_with_worktrees
    base_sha = run_cmd(["git", "rev-parse", "HEAD"], wt1_dir).stdout.strip()

    src_file = wt1_dir / "hello.py"
    src_file.write_text("def greet():\n    return 'hello superpowers'\n", encoding="utf-8")
    run_cmd(["git", "add", "hello.py"], wt1_dir)
    run_cmd(["git", "commit", "-m", "feat(iter-01): add greet function"], wt1_dir)
    head_sha = run_cmd(["git", "rev-parse", "HEAD"], wt1_dir).stdout.strip()

    pkg_path = generate_review_package(base_sha, head_sha, task_id="01-task", repo_dir=wt1_dir)
    assert pkg_path.exists()
    pkg_text = pkg_path.read_text(encoding="utf-8")
    assert "feat(iter-01): add greet function" in pkg_text
    assert "return 'hello superpowers'" in pkg_text

    porcelain = run_cmd(["git", "status", "--porcelain", "-uall"], wt1_dir).stdout.strip()
    assert porcelain == ""

def test_cli_guard_blocks_root_sync_on_feature_branch(git_repo_with_worktrees):
    """Validates that running iter_sync.py without --local on a feature branch refuses to touch root README."""
    _, wt1_dir, _ = git_repo_with_worktrees
    script_path = SCRIPTS_DIR / "iter_sync.py"
    res = run_cmd([sys.executable, str(script_path), str(wt1_dir)], cwd=wt1_dir, check=False)
    assert res.returncode != 0
    assert "Zero-Root-Touch" in (res.stderr + res.stdout)

def test_verify_todos_committed_guard_before_worktree(git_repo_with_worktrees):
    """
    Validates that uncommitted docs/todos files created by /iter init are detected by
    verify_todos_committed (--verify-committed) before spawning a new worktree.
    """
    repo_dir, _, _ = git_repo_with_worktrees

    # Initially clean and committed on main
    clean_res = verify_todos_committed(repo_dir)
    assert clean_res["committed"] is True
    assert clean_res["dirty_files"] == []

    # Simulate /iter init creating a new iteration 03-iter-three without committing yet
    iter3_dir = repo_dir / "docs" / "todos" / "03-iter-three"
    iter3_dir.mkdir()
    (iter3_dir / "README.md").write_text("# Iter 03\n", encoding="utf-8")
    (iter3_dir / "01-new-task.md").write_text("---\nstatus: '⚪ 待开始 (TODO)'\n---\n", encoding="utf-8")

    dirty_res = verify_todos_committed(repo_dir)
    assert dirty_res["committed"] is False
    assert any("03-iter-three" in f for f in dirty_res["dirty_files"])

    # Once committed on main, verify_todos_committed passes and new worktree receives the files
    run_cmd(["git", "add", "docs/todos/"], repo_dir)
    run_cmd(["git", "commit", "-m", "docs(iter): init 03-iter-three"], repo_dir)

    after_commit = verify_todos_committed(repo_dir)
    assert after_commit["committed"] is True
