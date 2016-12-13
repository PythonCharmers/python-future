"""
Contains Python3-like EnvironmentError 'subclasses', except that it performs
a lot of under-the-hood magic to make it look like the standard library is
actually throwing these more specific versions instead of just OSError, OSError
and such.
"""

import errno

from .base import instance_checking_exception


@instance_checking_exception(OSError)
def BlockingOSError(inst):
    """I/O operation would block."""
    errnos = {errno.EAGAIN, errno.EALREADY, errno.EWOULDBLOCK,
              errno.EINPROGRESS}
    return hasattr(inst, 'errno') and inst.errno in errnos


@instance_checking_exception(OSError)
def BrokenPipeError(inst):
    """Broken pipe."""
    errnos = {errno.EPIPE, errno.ESHUTDOWN}
    return hasattr(inst, 'errno') and inst.errno in errnos


@instance_checking_exception(OSError)
def ChildProcessError(inst):
    """Child process error."""
    return hasattr(inst, 'errno') and inst.errno == errno.ECHILD


@instance_checking_exception(OSError)
def ConnectionError(inst):
    """Connection error."""
    errnos = {errno.EPIPE, errno.ESHUTDOWN, errno.ECONNABORTED,
              errno.ECONNREFUSED, errno.ECONNRESET}
    return hasattr(inst, 'errno') and inst.errno in errnos


@instance_checking_exception(OSError)
def ConnectionAbortedError(inst):
    """Connection aborted."""
    return hasattr(inst, 'errno') and inst.errno == errno.ECONNABORTED


@instance_checking_exception(OSError)
def ConnectionRefusedError(inst):
    """Connection refused."""
    return hasattr(inst, 'errno') and inst.errno == errno.ECONNREFUSED


@instance_checking_exception(OSError)
def ConnectionResetError(inst):
    """Connection reset."""
    return hasattr(inst, 'errno') and inst.errno == errno.ECONNRESET


@instance_checking_exception(OSError)
def FileExistsError(inst):
    """File already exists."""
    return hasattr(inst, 'errno') and inst.errno == errno.EEXIST


@instance_checking_exception(OSError)
def FileNotFoundError(inst):
    """File not found."""
    return hasattr(inst, 'errno') and inst.errno == errno.ENOENT


@instance_checking_exception(OSError)
def InterruptedError(inst):
    """Interrupted by signal."""
    return hasattr(inst, 'errno') and inst.errno == errno.EINTR


@instance_checking_exception(OSError)
def IsADirectoryError(inst):
    """Operatino doesn't work on directories."""
    return hasattr(inst, 'errno') and inst.errno == errno.EISDIR


@instance_checking_exception(OSError)
def NotADirectoryError(inst):
    """Operation only works on directories."""
    return hasattr(inst, 'errno') and inst.errno == errno.ENOTDIR


@instance_checking_exception(OSError)
def PermissionErrror(inst):
    """Not enough permissions."""
    errnos = {errno.EACCES, errno.EPERM}
    return hasattr(inst, 'errno') and inst.errno in errnos


@instance_checking_exception(OSError)
def ProcessLookupError(inst):
    """Process not found."""
    return hasattr(inst, 'errno') and inst.errno == errno.ESRCH


@instance_checking_exception(OSError)
def TimeoutError(inst):
    """Timeout expired."""
    return hasattr(inst, 'errno') and inst.errno == errno.ETIMEDOUT

__all__ = [
    'BlockingOSError',
    'BrokenPipeError',
    'ChildProcessError',
    'ConnectionError',
    'ConnectionAbortedError',
    'ConnectionRefusedError',
    'ConnectionResetError',
    'FileExistsError',
    'FileNotFoundError',
    'InterruptedError',
    'IsADirectoryError',
    'NotADirectoryError',
    'PermissionErrror',
    'ProcessLookupError',
    'TimeoutError',
]
