"""CLI adapter. Query modules never depend on this layer."""
import json
import sys
import time
from pathlib import Path
from iter_sync import (
    audit_task_file, discover_task_files, parse_card, record_event,
    audit_scope_firewall, render_task_envelope, record_fix_and_check_fuse,
    resolve_target_iteration_dir, serve_live_board, generate_board_data,
    build_html_dashboard, render_terminal_board, generate_review_package,
    verify_todos_committed, check_branch_isolation, find_todos_root,
    resolve_local_iter_dir, sync_local_iteration, is_feature_or_worktree, sync_todos,
)


def main(argv: list[str] | None = None) -> int:
    """Run a command without terminating an importing caller."""
    try:
        _dispatch(sys.argv[1:] if argv is None else argv)
        return 0
    except SystemExit as error:
        return error.code
    except (OSError, ValueError, RuntimeError) as error:
        print(f"[IterSync:Error] {error}", file=sys.stderr)
        return 1


def _dispatch(argv):
    start_time = time.perf_counter()
    args = list(argv)
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
        print('Timing: --timing-init <trace> <session-id> | --timing-import <trace> <observation-json> | --timing-import-receipt <trace> <receipt> --category CATEGORY --operation OP --target TARGET | --timing-report <trace> | --timing-trace <trace> (inventory/preflight). Iteration Manager: --verify-committed | --takeover-report <iteration-dir> | --inventory <iteration-dir> --mode {continue,takeover} [--context JSON (--phase PHASE | --phase-from-context) --details] | --execution-report <iteration-dir> | --preflight <iteration-dir> [--context JSON (--phase PHASE | --phase-from-context) --owner OWNER] | --dispatch-check <card> [--context JSON --phase PHASE --owner OWNER] | --render-envelope <card> [repo] | --autonomy <action including attempt> <card> --event-id ID --owner OWNER | --check-scope BASE HEAD CARD [--include-worktree] | --review-pkg BASE HEAD [task] [repo] | --local [--strict] [path] | --check-branch [--strict] [repo] [base] | --board | --serve-board [port] [path] | --export-board [path]. See references/execution_readiness.md for opt-in readiness/attempt reports; references/agent_protocol.md for recovery and budgets.')
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
    sys.exit(main())
