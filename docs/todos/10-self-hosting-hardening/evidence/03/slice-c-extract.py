"""One-time bounded extraction; keeps the old dispatch body intact."""
from pathlib import Path

root = Path.cwd()
sync = root / 'scripts/iter_sync.py'
raw = sync.read_bytes()
text = raw.decode('utf-8').replace('\r\n', '\n')
prefix, rest = text.split('def main():\n', 1)
body = rest.split('\n\nif __name__ == "__main__":', 1)[0]
body = body.replace('    args = sys.argv[1:]\n', '    args = list(argv)\n', 1)
body = body.replace("print('Iteration Manager: ", "print('Timing: --timing-init <trace> <session-id> | --timing-import <trace> <observation-json> | --timing-import-receipt <trace> <receipt> --category CATEGORY --operation OP --target TARGET | --timing-report <trace> | --timing-trace <trace> (inventory/preflight). Iteration Manager: ", 1)
header = '''"""CLI adapter. Query modules never depend on this layer."""
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
'''
(root / 'scripts/iter_cli.py').write_text(header + body + '\n\n\nif __name__ == "__main__":\n    sys.exit(main())\n', encoding='utf-8')
facade = '''def main():
    """Compatibility entry point; importing iter_sync does not load the CLI."""
    from iter_cli import main as cli_main
    return cli_main()


if __name__ == "__main__":
    sys.exit(main())
'''
newline = '\r\n' if b'\r\n' in raw else '\n'
sync.write_bytes((prefix + facade).replace('\n', newline).encode('utf-8'))
