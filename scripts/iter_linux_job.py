"""Per-command Linux subreaper. The long-lived caller never becomes a subreaper.

The supervisor adopts orphan descendants; it signals only its own unreaped direct
children using pidfds, repeatedly reaps them, and proves emptiness with ECHILD.
"""
import ctypes
import json
import os
import select
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone


def stamp():
    return datetime.now(timezone.utc).isoformat()


def cleanup(children_path, root_pid, state):
    limit = time.monotonic() + 3.5
    while True:
        # Only unreaped direct children are signalled. Their pidfds pin identity.
        with open(children_path, encoding='ascii') as f:
            children = [int(item) for item in f.read().split()]
        for pid in children:
            try:
                fd = os.pidfd_open(pid)
                try:
                    signal.pidfd_send_signal(fd, signal.SIGKILL)
                finally:
                    os.close(fd)
            except ProcessLookupError:
                pass
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except ChildProcessError:
                return True
            if not pid:
                break
            if pid == root_pid and state['raw_exit_code'] is None:
                state['raw_exit_code'] = os.waitstatus_to_exitcode(status)
        if time.monotonic() >= limit:
            return False
        time.sleep(.01)


def supervise(child_path):
    state = {'status': 'PREPARING', 'raw_exit_code': None, 'started_at': None,
             'tree_terminal': False}
    interrupted = False
    def stop(_signum, _frame):
        nonlocal interrupted
        interrupted = True
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    cancellation_signals = {signal.SIGTERM, signal.SIGINT}
    # A supervisor must be able to handle cancellation even if its caller
    # inherited a blocked mask; this changes only this dedicated process.
    signal.pthread_sigmask(signal.SIG_UNBLOCK, cancellation_signals)
    with open(child_path, 'x', encoding='utf-8') as stream:
        def save():
            stream.seek(0); json.dump(state, stream); stream.truncate()
            stream.flush(); os.fsync(stream.fileno())
        try:
            libc = ctypes.CDLL(None, use_errno=True)
            if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER
                raise OSError(ctypes.get_errno(), 'PR_SET_CHILD_SUBREAPER failed')
            value = ctypes.c_int()
            if libc.prctl(37, ctypes.byref(value), 0, 0, 0) != 0 or value.value != 1:
                raise OSError('Cannot verify subreaper')
            children_path = f'/proc/self/task/{os.getpid()}/children'
            with open(children_path, encoding='ascii') as f:
                f.read()
            fd = os.pidfd_open(os.getpid())
            try:
                signal.pidfd_send_signal(fd, 0)
            finally:
                os.close(fd)
            state['status'] = 'READY'; save()
            # The caller retains this pipe for its lifetime. EOF requests cleanup.
            line = sys.stdin.buffer.readline()
            if not line or interrupted:
                state.update(status='NOT_STARTED', tree_terminal=True, ended_at=stamp()); save(); return
            request = json.loads(line)
            state['deadline_checked_at'] = stamp()
            launch_before = datetime.fromisoformat(request['launch_before'])
            # Serialize handled signals with the final launch decision. EOF is
            # ordered at its nonblocking observation; a later EOF or signal is
            # cancellation after launch has won and triggers tree cleanup.
            previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, cancellation_signals)
            try:
                readable, _, _ = select.select([sys.stdin], [], [], 0)
                caller_lost = bool(readable) and not os.read(sys.stdin.fileno(), 1)
                # Unexpected extra input is not part of the one-request protocol.
                if readable and not caller_lost:
                    raise ValueError('Unexpected data after launch request')
                canceled = interrupted or bool(signal.sigpending() & cancellation_signals)
                expired = datetime.now(timezone.utc) >= launch_before
                if caller_lost or canceled or expired:
                    state.update(status='NOT_STARTED', tree_terminal=True, ended_at=stamp())
                    save()
                    return
                # This pending-signal observation commits launch. Signals remain
                # blocked through Popen, and the child restores the prior mask.
                proc = subprocess.Popen(request['argv'], stdin=subprocess.DEVNULL, close_fds=True,
                                        preexec_fn=lambda: signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask))
                state.update(status='RUNNING', pid=proc.pid, started_at=stamp()); save()
            finally:
                signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
            root_done = False
            timed_out = False
            while not root_done and not interrupted:
                try:
                    pid, status = os.waitpid(proc.pid, os.WNOHANG)
                except ChildProcessError:
                    raise OSError('Root process wait failed')
                if pid:
                    state['raw_exit_code'] = os.waitstatus_to_exitcode(status)
                    root_done = True
                    break
                if datetime.now(timezone.utc) >= datetime.fromisoformat(request['launch_before']):
                    timed_out = True; break
                readable, _, _ = select.select([sys.stdin], [], [], .02)
                if readable and not os.read(sys.stdin.fileno(), 1):
                    interrupted = True
            state['status'] = 'CLEANING'; save()
            state['tree_terminal'] = cleanup(children_path, proc.pid, state)
            state.update(status=('CLEANUP_UNKNOWN' if not state['tree_terminal'] else
                                 'INTERRUPTED' if interrupted else 'TIMED_OUT' if timed_out else 'COMPLETED'),
                         ended_at=stamp())
            save()
        except Exception as error:
            if state['started_at'] is not None:
                try:
                    state['tree_terminal'] = cleanup(children_path, state['pid'], state)
                except Exception:
                    state['tree_terminal'] = False
            state.update(status='ERROR' if state['tree_terminal'] or state['started_at'] is None else 'CLEANUP_UNKNOWN',
                         error=str(error), ended_at=stamp())
            # Once launched, any unproved cleanup remains unknown.
            if state['started_at'] is None:
                state['tree_terminal'] = True
            save()


if __name__ == '__main__':
    supervise(sys.argv[1])
