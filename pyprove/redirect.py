import sys
import os
import io
import ctypes

from sys import platform

libc = ctypes.CDLL(None)

if platform == "linux" or platform == "linux2":
    c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')
    c_stderr = ctypes.c_void_p.in_dll(libc, 'stderr')
elif platform == "darwin":
    c_stdout = ctypes.c_void_p.in_dll(libc, '__stdoutp')
    c_stderr = ctypes.c_void_p.in_dll(libc, '__stderrp')
elif platform == "win32":
    c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')
    c_stderr = ctypes.c_void_p.in_dll(libc, 'stderr')


def redirect(std, fd):
    libc.fflush(c_stdout)
    libc.fflush(c_stderr)
    std_fd = std.fileno()
    std.close()
    os.dup2(fd, std_fd)
    return io.TextIOWrapper(os.fdopen(std_fd, "wb"))


def start(f_log, bar=None):
    s_log = open(f_log, mode="wb")
    dup_out = os.dup(sys.stdout.fileno())
    dup_err = os.dup(sys.stderr.fileno())
    sys.stdout = redirect(sys.stdout, s_log.fileno())
    sys.stderr = redirect(sys.stderr, s_log.fileno())
    if bar:
        bar.file = io.TextIOWrapper(os.fdopen(dup_err, "wb"))
    return (s_log, dup_out, dup_err)


def finish(s_log, dup_out, dup_err):
    sys.stdout = redirect(sys.stdout, dup_out)
    sys.stderr = redirect(sys.stderr, dup_err)
    os.close(dup_out)
    os.close(dup_err)
    s_log.close()

