import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def test_linux_public_cli_preserves_exit_and_raw_output(tmp_path):
    runner = Path(__file__).resolve().parents[1] / 'scripts' / 'iter_run.py'
    deadline = (datetime.now(timezone.utc) + timedelta(seconds=30)).isoformat()
    proc = subprocess.run([sys.executable, '-B', str(runner), '--deadline', deadline,
                           '--evidence', 'result.json', '--', sys.executable, '-c',
                           'print("linux raw output"); raise SystemExit(7)'],
                          cwd=tmp_path, capture_output=True, text=True)
    assert proc.returncode == 7, proc.stderr
    receipt = json.loads((tmp_path / 'result.json').read_text())
    assert receipt['status'] == 'COMPLETED'
    assert receipt['raw_exit_code'] == 7 and receipt['tree_terminal'] is True
    assert 'linux raw output' in (tmp_path / receipt['output']).read_text()

import os
import signal
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import iter_run

pytestmark = pytest.mark.skipif(sys.platform != 'linux', reason='Linux supervisor integration')


def deadline(seconds=20):
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()


@pytest.mark.parametrize('exit_code', [124, 125])
def test_business_exit_is_not_runner_failure(tmp_path, exit_code):
    assert iter_run.run_check([sys.executable, '-c', f'raise SystemExit({exit_code})'],
                              deadline(), 'result.json', tmp_path) == exit_code
    record = json.loads((tmp_path / 'result.json').read_text())
    assert record['status'] == 'COMPLETED' and record['raw_exit_code'] == exit_code
    assert record['tree_terminal'] is True


def test_short_deadline_never_launches(tmp_path):
    assert iter_run.run_check([sys.executable, '-c', 'open("spawned", "w").close()'],
                              deadline(2), 'short.json', tmp_path) == 124
    assert not (tmp_path / 'spawned').exists()
    assert json.loads((tmp_path / 'short.json').read_text())['status'] == 'NOT_STARTED'


def test_sidecar_collision_cannot_launch_or_overwrite(tmp_path):
    (tmp_path / 'result.json.child.json').write_text('untouched')
    with pytest.raises(FileExistsError):
        iter_run.run_check([sys.executable, '-c', 'open("spawned", "w").close()'],
                           deadline(), 'result.json', tmp_path)
    assert (tmp_path / 'result.json.child.json').read_text() == 'untouched'
    assert not (tmp_path / 'spawned').exists()


def test_setsid_deep_orphans_are_reaped_after_root_exit(tmp_path):
    leaf = 'import time; time.sleep(1); open("escaped", "w").close()'
    middle = f'import os,subprocess,sys,time; os.setsid(); subprocess.Popen([sys.executable,"-c",{leaf!r}]); time.sleep(20)'
    root = f'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",{middle!r}]); time.sleep(.2)'
    assert iter_run.run_check([sys.executable, '-c', root], deadline(), 'tree.json', tmp_path) == 0
    assert json.loads((tmp_path / 'tree.json').read_text())['tree_terminal'] is True
    time.sleep(1.2)
    assert not (tmp_path / 'escaped').exists()


def test_concurrent_calls_are_isolated(tmp_path):
    def run(n):
        return iter_run.run_check([sys.executable, '-c', f'import time; time.sleep(.2); print({n})'],
                                  deadline(), f'{n}.json', tmp_path)
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert list(pool.map(run, [1, 2])) == [0, 0]
    for n in (1, 2):
        record = json.loads((tmp_path / f'{n}.json').read_text())
        assert record['tree_terminal'] is True and record['status'] == 'COMPLETED'
        assert (tmp_path / record['output']).read_text().strip() == str(n)


def test_setup_failure_never_launches(tmp_path, monkeypatch):
    monkeypatch.setattr(iter_run.sys, 'executable', '/nonexistent/runner-python')
    assert iter_run.run_check(['/bin/sh', '-c', 'touch spawned'], deadline(), 'fail.json', tmp_path) == 125
    assert not (tmp_path / 'spawned').exists()
    assert json.loads((tmp_path / 'fail.json').read_text())['status'] == 'ERROR'


def test_sigterm_cleans_tree_and_records_error(tmp_path):
    runner = Path(iter_run.__file__)
    target = 'import time; open("started", "w").close(); time.sleep(1.5); open("escaped", "w").close(); time.sleep(30)'
    proc = subprocess.Popen([sys.executable, '-B', str(runner), '--deadline', deadline(), '--evidence', 'signal.json',
                             '--', sys.executable, '-c', target], cwd=tmp_path)
    try:
        until = time.monotonic() + 5
        while not (tmp_path / 'started').exists() and time.monotonic() < until:
            time.sleep(.02)
        assert (tmp_path / 'started').exists()
        proc.send_signal(signal.SIGTERM)
        assert proc.wait(timeout=5) == 125
        record = json.loads((tmp_path / 'signal.json').read_text())
        assert record['tree_terminal'] is True and record['status'] == 'ERROR'
        time.sleep(1.6)
        assert not (tmp_path / 'escaped').exists()
    finally:
        if proc.poll() is None:
            proc.terminate(); proc.wait(timeout=5)


def test_timeout_kills_setsid_deep_tree(tmp_path):
    leaf = 'import time; time.sleep(3); open("escaped", "w").close(); time.sleep(20)'
    middle = f'import os,subprocess,sys,time; os.setsid(); subprocess.Popen([sys.executable,"-c",{leaf!r}]); time.sleep(20)'
    root = f'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",{middle!r}]); time.sleep(20)'
    unrelated = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(20)'])
    try:
        assert iter_run.run_check([sys.executable, '-c', root], deadline(7), 'timeout.json', tmp_path) == 124
        record = json.loads((tmp_path / 'timeout.json').read_text())
        assert record['status'] == 'TIMED_OUT' and record['tree_terminal'] is True
        assert unrelated.poll() is None
        time.sleep(1.2)
        assert not (tmp_path / 'escaped').exists()
    finally:
        unrelated.terminate(); unrelated.wait(timeout=5)


def test_missing_supervisor_proof_is_cleanup_unknown(tmp_path, monkeypatch):
    fake = tmp_path / 'supervisor-exit'
    fake.write_text('#!/bin/sh\nexit 0\n')
    fake.chmod(0o700)
    monkeypatch.setattr(iter_run.sys, 'executable', str(fake))
    assert iter_run.run_check(['/bin/true'], deadline(), 'unknown.json', tmp_path) == 125
    record = json.loads((tmp_path / 'unknown.json').read_text())
    assert record['status'] == 'CLEANUP_UNKNOWN' and record['tree_terminal'] is False


def test_missing_pidfd_capability_refuses_target(tmp_path, monkeypatch):
    # Run the real supervisor with its kernel capability probe forced to fail.
    wrapper = tmp_path / 'python-without-pidfd'
    wrapper.write_text(f'#!{sys.executable}\n'
                       'import os, runpy, sys\n'
                       'def unavailable(*args): raise OSError("pidfd unavailable")\n'
                       'os.pidfd_open = unavailable\n'
                       'sys.argv = [sys.argv[2], sys.argv[3]]\n'
                       'runpy.run_path(sys.argv[0], run_name="__main__")\n')
    wrapper.chmod(0o700)
    monkeypatch.setattr(iter_run.sys, 'executable', str(wrapper))
    assert iter_run.run_check(['/bin/sh', '-c', 'touch spawned'], deadline(), 'capability.json', tmp_path) == 125
    assert not (tmp_path / 'spawned').exists()
    record = json.loads((tmp_path / 'capability.json').read_text())
    assert record['status'] == 'ERROR' and record['tree_terminal'] is True
    assert 'pidfd unavailable' in record['command']['error']


def test_killed_supervisor_never_proves_terminal(tmp_path):
    runner = Path(iter_run.__file__)
    target = 'import os,time; open("target-pid", "w").write(str(os.getpid())); time.sleep(30)'
    proc = subprocess.Popen([sys.executable, '-B', str(runner), '--deadline', deadline(), '--evidence', 'kill.json',
                             '--', sys.executable, '-c', target], cwd=tmp_path)
    fd = None
    try:
        until = time.monotonic() + 5
        while not (tmp_path / 'target-pid').exists() and time.monotonic() < until:
            time.sleep(.02)
        assert (tmp_path / 'target-pid').exists()
        fd = os.pidfd_open(int((tmp_path / 'target-pid').read_text()))
        record = json.loads((tmp_path / 'kill.json').read_text())
        os.kill(record['container_pid'], signal.SIGKILL)
        assert proc.wait(timeout=5) == 125
        record = json.loads((tmp_path / 'kill.json').read_text())
        assert record['status'] == 'CLEANUP_UNKNOWN' and record['tree_terminal'] is False
    finally:
        if fd is not None:
            try:
                signal.pidfd_send_signal(fd, signal.SIGKILL)
            except ProcessLookupError:
                pass
            os.close(fd)
        if proc.poll() is None:
            proc.terminate(); proc.wait(timeout=5)


def test_existing_output_is_not_overwritten(tmp_path):
    output = tmp_path / 'taken.json.output.txt'
    output.write_text('original')
    with pytest.raises(FileExistsError):
        iter_run.run_check(['/bin/sh', '-c', 'touch spawned'], deadline(), 'taken.json', tmp_path)
    assert output.read_text() == 'original'
    assert not (tmp_path / 'spawned').exists()


def test_unsupported_platform_rejects_before_target(tmp_path, monkeypatch):
    monkeypatch.setattr(iter_run.sys, 'platform', 'unsupported-test-platform')
    with pytest.raises(OSError):
        iter_run.run_check(['/bin/sh', '-c', 'touch spawned'], deadline(), 'unsupported.json', tmp_path)
    assert not (tmp_path / 'spawned').exists()
    assert not (tmp_path / 'unsupported.json').exists()


def test_concurrent_timeout_does_not_kill_other_call(tmp_path):
    def slow():
        return iter_run.run_check([sys.executable, '-c', 'import time; time.sleep(15)'],
                                  deadline(6), 'timeout.json', tmp_path)
    def other():
        return iter_run.run_check([sys.executable, '-c', 'import time; time.sleep(2); print("survived")'],
                                  deadline(), 'other.json', tmp_path)
    with ThreadPoolExecutor(max_workers=2) as pool:
        a, b = pool.submit(slow), pool.submit(other)
        assert a.result() == 124 and b.result() == 0
    assert json.loads((tmp_path / 'timeout.json').read_text())['status'] == 'TIMED_OUT'
    receipt = json.loads((tmp_path / 'other.json').read_text())
    assert receipt['status'] == 'COMPLETED' and receipt['tree_terminal'] is True
    assert (tmp_path / receipt['output']).read_text().strip() == 'survived'
