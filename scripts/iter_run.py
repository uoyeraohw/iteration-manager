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
    if os.name != 'nt':
        raise OSError('This runner requires Windows Job Objects; no command started')
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
