"""Windows Job container: attach a gated launcher before it can spawn work."""
import ctypes
import time
from ctypes import wintypes as w


class BasicLimits(ctypes.Structure):
    _fields_ = [('ProcessTime', ctypes.c_int64), ('JobTime', ctypes.c_int64),
                ('Flags', w.DWORD), ('MinWorkingSet', ctypes.c_size_t),
                ('MaxWorkingSet', ctypes.c_size_t), ('ActiveLimit', w.DWORD),
                ('Affinity', ctypes.c_size_t), ('Priority', w.DWORD), ('Scheduling', w.DWORD)]


class IoCounters(ctypes.Structure):
    _fields_ = [(name, ctypes.c_uint64) for name in ('ReadOps', 'WriteOps', 'OtherOps', 'ReadBytes', 'WriteBytes', 'OtherBytes')]


class ExtendedLimits(ctypes.Structure):
    _fields_ = [('Basic', BasicLimits), ('Io', IoCounters), ('ProcessMemory', ctypes.c_size_t),
                ('JobMemory', ctypes.c_size_t), ('PeakProcess', ctypes.c_size_t), ('PeakJob', ctypes.c_size_t)]


class Accounting(ctypes.Structure):
    _fields_ = [(name, ctypes.c_int64) for name in ('User', 'Kernel', 'PeriodUser', 'PeriodKernel')] + [
        (name, w.DWORD) for name in ('PageFaults', 'TotalProcesses', 'ActiveProcesses', 'TerminatedProcesses')]


class Job:
    def __init__(self):
        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        for name, args, result in [
            ('CreateJobObjectW', [w.LPVOID, w.LPCWSTR], w.HANDLE),
            ('SetInformationJobObject', [w.HANDLE, ctypes.c_int, w.LPVOID, w.DWORD], w.BOOL),
            ('AssignProcessToJobObject', [w.HANDLE, w.HANDLE], w.BOOL),
            ('QueryInformationJobObject', [w.HANDLE, ctypes.c_int, w.LPVOID, w.DWORD, w.LPVOID], w.BOOL),
            ('TerminateJobObject', [w.HANDLE, w.UINT], w.BOOL),
            ('CloseHandle', [w.HANDLE], w.BOOL),
        ]:
            fn = getattr(self.api, name)
            fn.argtypes, fn.restype = args, result
        self.handle = self.api.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = ExtendedLimits()
        limits.Basic.Flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            error = ctypes.WinError(ctypes.get_last_error())
            self.close()
            raise error

    def attach(self, process):
        if not self.api.AssignProcessToJobObject(self.handle, int(process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())

    def active(self):
        info = Accounting()
        if not self.api.QueryInformationJobObject(self.handle, 1, ctypes.byref(info), ctypes.sizeof(info), None):
            raise ctypes.WinError(ctypes.get_last_error())
        return info.ActiveProcesses

    def stop(self, seconds=3):
        if not self.api.TerminateJobObject(self.handle, 124):
            raise ctypes.WinError(ctypes.get_last_error())
        until = time.monotonic() + seconds
        while self.active():
            if time.monotonic() >= until:
                return False
            time.sleep(.02)
        return True

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle)
            self.handle = None
