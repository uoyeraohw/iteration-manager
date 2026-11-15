"""Exercise the actual whitelist payload without maintenance history."""
import json
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from iter_install import _inventory


def test_payload_copy_runs_handoff_and_service_with_frozen_runner(tmp_path):
    payload = tmp_path / 'payload'
    payload.mkdir()
    inventory = _inventory(ROOT)
    assert 'tests/support/browser_harness.py' in inventory
    assert not any(p.startswith('docs/') for p in inventory)
    for name in sorted(inventory):
        target = payload / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    assert not (payload / 'docs/todos').exists()
    runner = Path(os.environ.get('ITER_FROZEN_RUNNER', str(ROOT / 'scripts/iter_run.py')))
    assert runner.is_absolute() and runner.is_file()
    receipt = 'installed-copy-receipt.json'
    args = [sys.executable, '-B', str(runner), '--deadline', os.environ.get('ITER_COMMAND_DEADLINE',
            (datetime.now(timezone.utc) + timedelta(minutes=2)).isoformat()),
            '--evidence', receipt, '--', sys.executable, '-B', '-m', 'pytest',
            '-p', 'no:cacheprovider', 'tests/test_board_handoff.py', 'tests/test_board_service.py',
            '-q', '--basetemp', str(tmp_path / 'installed-pytest')]
    result = subprocess.run(args, cwd=payload, capture_output=True, text=True, timeout=45)
    record = json.loads((payload / receipt).read_text(encoding='utf-8'))
    output = (payload / record['output']).read_text(encoding='utf-8')
    assert result.returncode == 0, (result.stdout, result.stderr, record, output)
    assert record['status'] == 'COMPLETED' and record['tree_terminal'] is True
    # Pytest exits 5 for an empty collection; exit 0 establishes successful tests.
    assert record['raw_exit_code'] == 0 and output.strip()
    assert not (payload / 'docs/todos').exists()
    check_arguments(payload / 'tests/support/browser_harness.py', tmp_path)


def check_arguments(script, tmp_path):
    help_result = subprocess.run([sys.executable, '-B', str(script), '--help'], capture_output=True, text=True)
    assert help_result.returncode == 0
    assert all(arg in help_result.stdout for arg in ('--ready-file', '--stop-file', '--duration', '--delay', '--isolated-fixtures'))
    ready, stop = tmp_path / 'ready', tmp_path / 'stop'
    args = [sys.executable, '-B', str(script), '--ready-file', str(ready), '--stop-file', str(stop)]
    for invalid in (['--duration', '0'], ['--delay', '-1']):
        result = subprocess.run(args + invalid, capture_output=True, text=True)
        assert result.returncode == 2 and 'duration must be positive' in result.stderr
        assert not ready.exists() and not stop.exists()
    ready.touch()
    result = subprocess.run(args, capture_output=True, text=True)
    assert result.returncode == 2 and 'existing files are not overwritten' in result.stderr


def test_harness_argument_errors_and_help(tmp_path):
    check_arguments(ROOT / 'tests/support/browser_harness.py', tmp_path)
