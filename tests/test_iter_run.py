import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import iter_run


def deadline(seconds=20):
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()


def test_actual_exit_and_raw_output(tmp_path):
    result = iter_run.run_check([sys.executable, '-c', 'print("raw output"); raise SystemExit(7)'], deadline(), 'run.json', tmp_path)
    assert result == 7
    receipt = json.loads((tmp_path/'run.json').read_text())
    assert receipt['status'] == 'COMPLETED' and receipt['raw_exit_code'] == 7
    assert receipt['deadline_checked_at'] <= receipt['started_at'] <= receipt['ended_at']
    assert receipt['tree_terminal'] is True
    assert 'raw output' in (tmp_path/receipt['output']).read_text()


def test_expired_does_not_spawn(tmp_path):
    code = 'from pathlib import Path; Path("side-effect").touch()'
    assert iter_run.run_check([sys.executable, '-c', code], deadline(-1), 'expired.json', tmp_path) == 124
    assert not (tmp_path/'side-effect').exists()
    receipt = json.loads((tmp_path/'expired.json').read_text())
    assert receipt['status'] == 'NOT_STARTED' and receipt['raw_exit_code'] is None


def test_evidence_never_overwritten(tmp_path):
    (tmp_path/'old.json').write_text('original')
    with pytest.raises(FileExistsError):
        iter_run.run_check([sys.executable, '-c', 'open("side-effect","w").close()'], deadline(), 'old.json', tmp_path)
    assert (tmp_path/'old.json').read_text() == 'original'
    assert not (tmp_path/'side-effect').exists()


def test_timeout_kills_descendants_and_does_not_touch_unrelated(tmp_path):
    unrelated = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(40)'])
    child_code = 'import time; from pathlib import Path; time.sleep(9); Path("escaped").touch(); time.sleep(30)'
    code = f'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",{child_code!r}]); time.sleep(30)'
    try:
        start = time.monotonic()
        assert iter_run.run_check([sys.executable, '-c', code], deadline(7), 'timeout.json', tmp_path) == 124
        assert time.monotonic() - start < 9
        receipt = json.loads((tmp_path/'timeout.json').read_text())
        assert receipt['status'] == 'TIMED_OUT' and receipt['tree_terminal'] is True
        assert unrelated.poll() is None
        time.sleep(9)
        assert not (tmp_path/'escaped').exists()
    finally:
        unrelated.terminate(); unrelated.wait(timeout=5)


def test_cli_and_no_implicit_shell(tmp_path):
    script = Path(iter_run.__file__)
    argv = [sys.executable, '-B', str(script), '--deadline', deadline(), '--evidence', 'cli.json', '--',
            sys.executable, '-c', 'import sys; print(sys.argv[1]); raise SystemExit(7)', 'x; echo NOT_A_SHELL']
    proc = subprocess.run(argv, cwd=tmp_path, capture_output=True, text=True)
    assert proc.returncode == 7, proc.stdout + proc.stderr
    receipt = json.loads((tmp_path/'cli.json').read_text())
    assert receipt['argv'][-1] == 'x; echo NOT_A_SHELL'


def test_parent_exit_does_not_let_orphan_escape(tmp_path):
    descendant = 'import time; from pathlib import Path; time.sleep(2); Path("orphan").touch()'
    code = f'import subprocess,sys; subprocess.Popen([sys.executable,"-c",{descendant!r}])'
    assert iter_run.run_check([sys.executable, '-c', code], deadline(), 'orphan.json', tmp_path) == 0
    assert json.loads((tmp_path/'orphan.json').read_text())['tree_terminal']
    time.sleep(2.5)
    assert not (tmp_path/'orphan').exists()


def test_cleanup_unknown_cannot_pass_business_exit(tmp_path, monkeypatch):
    import iter_win_job
    original = iter_win_job.Job.stop
    def uncertain(self, seconds=3):
        original(self, seconds)
        return False
    monkeypatch.setattr(iter_win_job.Job, 'stop', uncertain)
    assert iter_run.run_check([sys.executable, '-c', 'pass'], deadline(), 'unknown.json', tmp_path) == 125
    record = json.loads((tmp_path/'unknown.json').read_text())
    assert record['status'] == 'CLEANUP_UNKNOWN' and record['raw_exit_code'] == 0


def test_attachment_failure_never_launches_target(tmp_path, monkeypatch):
    import iter_win_job
    def refuse(self, process):
        raise OSError('attachment denied')
    monkeypatch.setattr(iter_win_job.Job, 'attach', refuse)
    assert iter_run.run_check([sys.executable, '-c', 'open("launched","w").close()'], deadline(), 'attach.json', tmp_path) == 125
    assert not (tmp_path/'launched').exists()
    assert json.loads((tmp_path/'attach.json').read_text())['raw_exit_code'] is None


@pytest.mark.parametrize('path', ['../escape.json', '/absolute.json'])
def test_evidence_stays_in_workspace(tmp_path, path):
    with pytest.raises(ValueError):
        iter_run.run_check([sys.executable, '-c', 'pass'], deadline(), path, tmp_path)
