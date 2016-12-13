"""
This module is designed to be used as follows::

    from future.builtins.exceptions import (FileNotFoundError, FileExistsError)

And then, for example::

        try:
            args.func(args)
        except FileExistsError as e:
            parser.error('Refusing to clobber existing path ({err})'.format(err=e))

Note that this is standard Python 3 code, plus some imports that do
nothing on Python 3.

The exceptions this brings in are::

- ``FileNotFoundError``
- ``FileExistsError``

"""

from __future__ import division, absolute_import, print_function

import errno
import os
import sys

from future.utils import with_metaclass


class BaseNewFileNotFoundError(type):
    def __instancecheck__(cls, instance):
        return hasattr(instance, 'errno') and instance.errno == errno.ENOENT

    def __subclasscheck__(cls, classinfo):
        # This hook is called during the exception handling.
        # Unfortunately, we would rather have exception handling call
        # __instancecheck__, so we have to do that ourselves. But,
        # that's not how it currently is.  If you feel like proposing a
        # patch for Python, check the function
        # `PyErr_GivenExceptionMatches` in `Python/error.c`.
        value = sys.exc_info()[1]

        # Double-check that the exception given actually somewhat
        # matches the classinfo we received. If not, people are using
        # `issubclass` directly, which is of course prone to errors.
        if value.__class__ != classinfo:
            print('Mismatch!\nvalue: {0}\nvalue.__class__: {1}\nclassinfo: {2}'.format(
                value, value.__class__, classinfo)
            )

        return isinstance(value, cls)


class NewFileNotFoundError(with_metaclass(BaseNewFileNotFoundError, IOError)):
    """
    A backport of the Python 3.3+ FileNotFoundError to Py2
    """
    def __init__(self, *args, **kwargs):
        print('ARGS ARE: {}'.format(args))
        print('KWARGS ARE: {}'.format(kwargs))
        super(NewFileNotFoundError, self).__init__(*args, **kwargs)  # cls, *args, **kwargs)
        self.errno = errno.ENOENT
        
    def __str__(self):
        # return 'FILE NOT FOUND!'
        return self.message or os.strerror(self.errno)

    def __native__(self):
        """
        Hook for the future.utils.native() function
        """
        err = IOError(self.message)
        err.errno = self.errno
        return err


# try:
#     FileNotFoundError
# except NameError:
#     # Python < 3.3
#     class FileNotFoundError(IOError):
#         def __init__(self, message=None, *args):
#             super(FileNotFoundError, self).__init__(args)
#             self.message = message
#             self.errno = errno.ENOENT
# 
#         def __str__(self):
#             return self.message or os.strerror(self.errno)


__all__ = ['NewFileNotFoundError']
