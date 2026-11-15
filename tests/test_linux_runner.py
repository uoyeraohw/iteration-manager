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


@pytest.mark.parametrize('event', ['sigterm', 'caller_eof'])
def test_prelaunch_cancellation_wins_after_request_consumption(tmp_path, event):
    """A real supervisor pauses inside the first timestamp after parsing the request."""
    scripts = Path(iter_run.__file__).parent
    worker = '''
import os, sys, time, signal
sys.path.insert(0, sys.argv[1])
import iter_linux_job as job
original_signal = signal.signal
def register(signum, handler):
    if signum == signal.SIGTERM:
        def observed(signum, frame):
            handler(signum, frame)
            open(sys.argv[5], 'w').close()
        return original_signal(signum, observed)
    return original_signal(signum, handler)
signal.signal = register
original = job.stamp
first = True
def gate_stamp():
    global first
    if first:
        first = False
        open(sys.argv[3], 'w').close()
        until = time.monotonic() + 5
        while not os.path.exists(sys.argv[4]):
            if time.monotonic() > until:
                raise RuntimeError('test gate timed out')
            time.sleep(.005)
    return original()
job.stamp = gate_stamp
job.supervise(sys.argv[2])
'''
    child = tmp_path / 'child.json'
    entered = tmp_path / 'entered'
    release = tmp_path / 'release'
    target = tmp_path / 'target-effect'
    handled = tmp_path / 'signal-handled'
    proc = subprocess.Popen([sys.executable, '-B', '-c', worker, str(scripts), str(child),
                             str(entered), str(release), str(handled)], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        until = time.monotonic() + 5
        while time.monotonic() < until:
            try:
                if json.loads(child.read_text())['status'] == 'READY':
                    break
            except (OSError, ValueError, KeyError):
                pass
            assert proc.poll() is None, proc.stderr.read().decode()
            time.sleep(.01)
        else:
            pytest.fail('supervisor did not reach READY')
        request = {'argv': [sys.executable, '-c', f'open({str(target)!r}, "w").close()'],
                   'launch_before': deadline(20)}
        proc.stdin.write((json.dumps(request) + '\n').encode()); proc.stdin.flush()
        until = time.monotonic() + 5
        while not entered.exists() and time.monotonic() < until:
            time.sleep(.01)
        assert entered.exists(), 'supervisor did not consume request'
        if event == 'sigterm':
            proc.send_signal(signal.SIGTERM)
            until = time.monotonic() + 5
            while not handled.exists() and time.monotonic() < until:
                time.sleep(.005)
            assert handled.exists(), 'supervisor did not handle SIGTERM before release'
        else:
            proc.stdin.close()
        release.touch()
        assert proc.wait(timeout=5) == 0
        record = json.loads(child.read_text())
        assert record['started_at'] is None and record.get('pid') is None, record
        assert record['status'] == 'NOT_STARTED' and record['tree_terminal'] is True
        assert not target.exists()
    finally:
        release.touch(exist_ok=True)
        if proc.stdin and not proc.stdin.closed:
            proc.stdin.close()
        if proc.poll() is None:
            proc.terminate(); proc.wait(timeout=5)
        proc.stdout.close(); proc.stderr.close()


@pytest.mark.parametrize('timing', ['pending_at_gate', 'after_launch_decision', 'caller_eof_after_decision'])
def test_cancellation_order_around_final_gate(tmp_path, timing):
    """Inject into the real supervisor with SIGTERM blocked at the gate."""
    scripts = Path(iter_run.__file__).parent
    worker = '''
import os, signal, sys, time
sys.path.insert(0, sys.argv[1])
import iter_linux_job as job
if sys.argv[3] == 'pending_at_gate':
    original = job.select.select
    def inject(*args):
        assert signal.SIGTERM in signal.pthread_sigmask(signal.SIG_BLOCK, set())
        os.kill(os.getpid(), signal.SIGTERM)
        return original(*args)
    job.select.select = inject
else:
    original = job.subprocess.Popen
    def inject(*args, **kwargs):
        assert signal.SIGTERM in signal.pthread_sigmask(signal.SIG_BLOCK, set())
        if sys.argv[3] == 'caller_eof_after_decision':
            open(sys.argv[4], 'w').close()
            until = time.monotonic() + 5
            while not os.path.exists(sys.argv[5]):
                if time.monotonic() > until: raise RuntimeError('gate wait timed out')
                time.sleep(.005)
        else:
            os.kill(os.getpid(), signal.SIGTERM)
        return original(*args, **kwargs)
    job.subprocess.Popen = inject
job.supervise(sys.argv[2])
'''
    child = tmp_path / 'child.json'
    entered = tmp_path / 'decision-won'
    release = tmp_path / 'release-decision'
    proc = subprocess.Popen([sys.executable, '-B', '-c', worker, str(scripts), str(child), timing,
                             str(entered), str(release)],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        until = time.monotonic() + 5
        while time.monotonic() < until:
            try:
                if json.loads(child.read_text())['status'] == 'READY':
                    break
            except (OSError, ValueError, KeyError):
                pass
            if proc.poll() is not None:
                pytest.fail('supervisor exited before READY: ' + proc.stderr.read().decode())
            time.sleep(.01)
        else:
            pytest.fail('supervisor did not reach READY')
        request = {'argv': [sys.executable, '-c', 'import time; time.sleep(10)'],
                   'launch_before': deadline(20)}
        proc.stdin.write((json.dumps(request) + '\n').encode()); proc.stdin.flush()
        if timing == 'caller_eof_after_decision':
            until = time.monotonic() + 5
            while not entered.exists() and time.monotonic() < until:
                time.sleep(.005)
            assert entered.exists(), 'launch decision did not complete'
            proc.stdin.close()
            release.touch()
        assert proc.wait(timeout=5) == 0
        record = json.loads(child.read_text())
        assert record['tree_terminal'] is True
        if timing == 'pending_at_gate':
            assert record['status'] == 'NOT_STARTED' and record['started_at'] is None
            assert record.get('pid') is None
        else:
            assert record['status'] == 'INTERRUPTED' and record['started_at'] is not None
            assert record.get('pid') is not None
    finally:
        release.touch(exist_ok=True)
        if proc.stdin and not proc.stdin.closed:
            proc.stdin.close()
        if proc.poll() is None:
            proc.terminate(); proc.wait(timeout=5)
        proc.stdout.close(); proc.stderr.close()


def test_target_does_not_inherit_gate_signal_mask(tmp_path):
    code = ('import signal, sys; '
            'blocked = signal.pthread_sigmask(signal.SIG_BLOCK, set()); '
            'sys.exit(9 if signal.SIGTERM in blocked or signal.SIGINT in blocked else 0)')
    assert iter_run.run_check([sys.executable, '-c', code], deadline(), 'mask.json', tmp_path) == 0
    record = json.loads((tmp_path / 'mask.json').read_text())
    assert record['status'] == 'COMPLETED' and record['tree_terminal'] is True
