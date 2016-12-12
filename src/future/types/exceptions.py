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
import itertools

from future.utils import with_metaclass


class BaseNewFileNotFoundError(type):
    def __instancecheck__(cls, instance):
        if cls == NewFileNotFoundError:
            # Special case for Py2 short or long int
            if isinstance(instance, IOError):
                return 'errno' in dir(e) and e.errno == errno.ENOENT
        else:
            return issubclass(instance.__class__, cls)


class NewFileNotFoundError(with_metaclass(BaseNewFileNotFoundError, IOError)):
    """
    A backport of the Python 3.3+ FileNotFoundError to Py2
    """
    def __new__(cls, *args, **kwargs):
        """
        """
        err = super(NewFileNotFoundError, cls).__new__(cls, *args, **kwargs)
        err.errno = errno.ENOENT
        return err
        
    def __str__(self):
        return self.message or os.strerror(self.errno)

    def __native__(self):
        """
        Hook for the future.utils.native() function
        """
        return IOError(self)


__all__ = ['NewFileNotFoundError']
