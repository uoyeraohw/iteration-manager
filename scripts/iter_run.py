"""Deadline-bound argv execution. Exit124 is timeout; exit125 is runner/cleanup error.

Receipts distinguish these outcomes from a command that itself exits124/125.
Interrupted RUNNING receipts remain unknown, never synthesized into completion.
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from iter_checkpoint import utc
from iter_contracts import relative_path

CLEANUP_RESERVE_SECONDS = 5

# The launcher cannot spawn the command before its parent attaches the Job and
# sends this one-line gate message. Its own terminal exit is not the command exit.
BOOTSTRAP = '''import json,os,subprocess,sys
from datetime import datetime,timezone
def now(): return datetime.now(timezone.utc).isoformat()
request=json.loads(sys.stdin.readline())
with open(request['child'], 'x', encoding='utf-8') as f:
    record={'status':'STARTING','raw_exit_code':None,'started_at':None,'pid':None}
    def save():
        f.seek(0); json.dump(record,f); f.truncate(); f.flush(); os.fsync(f.fileno())
    save()
    try:
        checked=datetime.now(timezone.utc)
        record['deadline_checked_at']=checked.isoformat()
        if checked >= datetime.fromisoformat(request['launch_before']):
            record.update(status='NOT_STARTED',ended_at=now()); save(); sys.exit(0)
        proc=subprocess.Popen(request['argv'],shell=False,close_fds=True,stdin=subprocess.DEVNULL)
        record.update(status='RUNNING',pid=proc.pid,started_at=now()); save()
        code=proc.wait()
        record.update(status='COMPLETED',raw_exit_code=code,ended_at=now()); save()
    except OSError as error:
        record.update(status='ERROR',error=str(error),ended_at=now()); save()
'''


def now():
    return datetime.now(timezone.utc)


def run_check(argv, deadline, evidence, cwd=None):
    if os.name != 'nt' and sys.platform != 'linux':
        raise OSError('Unsupported platform; no command started')
    if not isinstance(argv, (list, tuple)) or not argv or any(not isinstance(x, str) or '\0' in x for x in argv):
        raise ValueError('Nonempty argv list of text required')
    end = utc(deadline)
    root = Path(cwd or Path.cwd()).resolve(strict=True)
    rel = relative_path(str(evidence))
    receipt = (root / rel).resolve()
    if not receipt.is_relative_to(root):
        raise ValueError('Evidence leaves workspace')
    receipt.parent.mkdir(parents=True, exist_ok=True)
    output = receipt.with_name(receipt.name + '.output.txt')
    child = receipt.with_name(receipt.name + '.child.json')
    record = dict(version=1, argv=list(argv), cwd=str(root), deadline=end.isoformat(),
                  cleanup_reserve_seconds=CLEANUP_RESERVE_SECONDS, status='PREPARING',
                  deadline_checked_at=None, started_at=None, ended_at=None, raw_exit_code=None,
                  tree_terminal=False, output=output.relative_to(root).as_posix())
    # Exclusive reservation also survives caller interruption. Never reopen with w.
    with receipt.open('x', encoding='utf-8') as rf:
        def save():
            rf.seek(0); json.dump(record, rf, ensure_ascii=False, indent=2)
            rf.truncate(); rf.flush(); os.fsync(rf.fileno())
        save()
        if child.exists():
            record.update(status='NOT_STARTED', error='Child evidence already exists', ended_at=now().isoformat())
            save()
            raise FileExistsError(child)
        with output.open('x', encoding='utf-8') as log:
            checked = now()
            record['deadline_checked_at'] = checked.isoformat()
            remaining = (end - checked).total_seconds() - CLEANUP_RESERVE_SECONDS
            if remaining <= 0:
                record.update(status='NOT_STARTED', tree_terminal=True, ended_at=now().isoformat())
                save()
                return 124
            if sys.platform == 'linux':
                return run_linux(argv, end, root, child, log, record, save)
            proc, job = None, None
            cleanup_attempted = False
            timed_out = False
            wrapper_code = 125
            try:
                record['status'] = 'RUNNING'; save()
                from iter_win_job import Job
                job = Job()
                proc = subprocess.Popen([sys.executable, '-B', '-c', BOOTSTRAP], cwd=root,
                                        stdin=subprocess.PIPE, stdout=log, stderr=subprocess.STDOUT,
                                        close_fds=True, creationflags=subprocess.CREATE_NO_WINDOW)
                job.attach(proc)
                record['container_pid'] = proc.pid
                checked = now()
                record['deadline_checked_at'] = checked.isoformat()
                if (end - checked).total_seconds() <= CLEANUP_RESERVE_SECONDS:
                    record['status'] = 'NOT_STARTED'
                    timed_out = True
                else:
                    from datetime import timedelta
                    request = dict(argv=list(argv), child=str(child), launch_before=(end-timedelta(seconds=CLEANUP_RESERVE_SECONDS)).isoformat())
                    proc.stdin.write((json.dumps(request)+'\n').encode('utf-8'))
                    proc.stdin.close()
                if proc and not timed_out:
                    remaining = max(0, (end-now()).total_seconds()-CLEANUP_RESERVE_SECONDS)
                    try:
                        proc.wait(timeout=remaining)
                    except subprocess.TimeoutExpired:
                        timed_out = True
                if job:
                    record['tree_terminal'] = job.stop()
                    cleanup_attempted = True
                else:
                    record['tree_terminal'] = True
                if proc:
                    proc.wait(timeout=1)
                    record['launcher_exit_code'] = proc.returncode
                if child.exists():
                    try:
                        details = json.loads(child.read_text(encoding='utf-8'))
                    except ValueError:
                        if not timed_out:
                            raise
                        details = dict(status='UNKNOWN', error='Interrupted child evidence write')
                    record['command'] = details
                    if details.get('status') == 'NOT_STARTED':
                        timed_out = True
                    for key in ('raw_exit_code', 'started_at', 'deadline_checked_at'):
                        if details.get(key) is not None:
                            record[key] = details[key]
                if not record['tree_terminal']:
                    record['status'] = 'CLEANUP_UNKNOWN'
                elif timed_out:
                    record['status'] = 'TIMED_OUT' if record['started_at'] else 'NOT_STARTED'
                    wrapper_code = 124
                elif record['raw_exit_code'] is not None:
                    record['status'] = 'COMPLETED'
                    wrapper_code = record['raw_exit_code']
                else:
                    record['status'] = 'ERROR'
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                record.update(status='ERROR', error=str(error))
            finally:
                if job and not cleanup_attempted:
                    try:
                        record['tree_terminal'] = job.stop()
                    except OSError as error:
                        record.update(tree_terminal=False, cleanup_error=str(error))
                if job:
                    job.close()
                if proc:
                    if proc.stdin and not proc.stdin.closed:
                        proc.stdin.close()
                    if proc.poll() is None:
                        proc.kill()
                    try:
                        proc.wait(timeout=1)
                    except subprocess.TimeoutExpired:
                        record['tree_terminal'] = False
                if not record['tree_terminal']:
                    record['status'] = 'CLEANUP_UNKNOWN'; wrapper_code = 125
                record['ended_at'] = now().isoformat()
                record['late_by_seconds'] = max(0, (utc(record['ended_at']) - end).total_seconds())
                save()
            return wrapper_code


def run_linux(argv, end, root, child, log, record, save):
    """Start a gated supervisor, and accept completion only with its proof."""
    import signal
    import threading
    import time
    from datetime import timedelta
    proc = None
    interrupted = []
    old_handlers = {}
    try:
        if threading.current_thread() is threading.main_thread():
            def handle(signum, _frame):
                interrupted.append(signum)
                if proc is not None and proc.poll() is None:
                    try:
                        proc.send_signal(signal.SIGTERM)
                    except ProcessLookupError:
                        pass
            for sig in (signal.SIGTERM, signal.SIGINT):
                old_handlers[sig] = signal.getsignal(sig)
                signal.signal(sig, handle)
        record['status'] = 'RUNNING'; save()
        supervisor = Path(__file__).with_name('iter_linux_job.py')
        proc = subprocess.Popen([sys.executable, '-B', str(supervisor), str(child)],
                                cwd=root, stdin=subprocess.PIPE, stdout=log,
                                stderr=subprocess.STDOUT, close_fds=True)
        record['container_pid'] = proc.pid; save()
        if interrupted and proc.poll() is None:
            proc.send_signal(signal.SIGTERM)
        details = {}
        launch_before = end - timedelta(seconds=CLEANUP_RESERVE_SECONDS)
        while now() < launch_before and proc.poll() is None and not interrupted:
            try:
                details = json.loads(child.read_text(encoding='utf-8'))
            except (OSError, ValueError):
                time.sleep(.01); continue
            if details.get('status') != 'PREPARING':
                break
            time.sleep(.01)
        if details.get('status') == 'READY' and not interrupted and now() < launch_before:
            request = dict(argv=list(argv), launch_before=launch_before.isoformat())
            proc.stdin.write((json.dumps(request)+'\n').encode()); proc.stdin.flush()
        else:
            proc.stdin.close()
        remaining = max(0, (end-now()).total_seconds())
        try:
            proc.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            proc.kill(); proc.wait(timeout=1)
        record['launcher_exit_code'] = proc.returncode
        try:
            details = json.loads(child.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            details = {}
        record['command'] = details
        for key in ('raw_exit_code', 'started_at', 'deadline_checked_at'):
            if details.get(key) is not None:
                record[key] = details[key]
        record['tree_terminal'] = details.get('tree_terminal') is True and proc.returncode == 0
        status = details.get('status')
        if not record['tree_terminal']:
            record['status'] = 'CLEANUP_UNKNOWN'
            result = 125
        elif interrupted or status in ('INTERRUPTED', 'ERROR'):
            record['status'] = 'ERROR'; result = 125
        elif status in ('TIMED_OUT', 'NOT_STARTED'):
            record['status'] = status; result = 124
        elif status == 'COMPLETED' and record['raw_exit_code'] is not None:
            record['status'] = 'COMPLETED'; result = record['raw_exit_code']
        else:
            record['status'] = 'ERROR'; result = 125
        return result
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        record.update(status='CLEANUP_UNKNOWN' if proc else 'ERROR', error=str(error), tree_terminal=False)
        return 125
    finally:
        if proc:
            if proc.stdin and not proc.stdin.closed:
                proc.stdin.close()
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=max(0, (end-now()).total_seconds()))
                except subprocess.TimeoutExpired:
                    proc.kill(); proc.wait()
                record.update(status='CLEANUP_UNKNOWN', tree_terminal=False)
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)
        record['ended_at'] = now().isoformat()
        record['late_by_seconds'] = max(0, (utc(record['ended_at']) - end).total_seconds())
        save()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--deadline', required=True)
    parser.add_argument('--evidence', required=True)
    parser.add_argument('argv', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.argv[1:] if args.argv[:1] == ['--'] else args.argv
    try:
        return run_check(argv, args.deadline, args.evidence)
    except (OSError, ValueError) as error:
        print(json.dumps(dict(runner_error=str(error))), file=sys.stderr)
        return 125


if __name__ == '__main__':
    sys.exit(main())
