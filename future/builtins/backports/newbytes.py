"""
Pure-Python implementation of a Python 3-like bytes object for Python 2.

Why do this? Without it, the Python 2 bytes object is a very, very
different beast to the Python 3 bytes object. Running the
test_bytes_from_py33.py script from the Python 3.3 test suite using
Python 2 with its default str-aliased bytes object (after the appropriate
import fixes, and using the backported test.support module) yields this:
    ------------------------------------------------------------------
    Ran 203 tests in 0.214s
    
    FAILED (failures=31, errors=55, skipped=1)
    ------------------------------------------------------------------
when running

    $ python -m future.tests.test_bytes_from_py33

"""

import functools
from collections import Iterable

from future.utils import PY3

_builtin_bytes = bytes


def issubset(list1, list2):
    """
    Examples:

    >>> issubset([], [65, 66, 67])
    True
    >>> issubset([65], [65, 66, 67])
    True
    >>> issubset([65, 66], [65, 66, 67])
    True
    >>> issubset([65, 67], [65, 66, 67])
    False
    """
    n = len(list1)
    for startpos in range(len(list2) - n + 1):
        if list2[startpos:startpos+n] == list1:
            return True
    return False


def disallow_types(argnums, disallowed_types):
    """
    Example use:

    >>> class bytes(object):
    ...     @disallow_types([1], [unicode])
    ...     def __add__(self, other):
    ...          pass

    >>> newbytes('1234') + u'1234'      #doctest: +IGNORE_EXCEPTION_DETAIL 
    Traceback (most recent call last):
      ...
    TypeError: can't concat 'bytes' to (unicode) str
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            errmsg = "argument can't be unicode string"
            for (argnum, mytype) in zip(argnums, disallowed_types):
                if isinstance(args[argnum], mytype):
                    raise TypeError(errmsg)

            return function(*args, **kwargs)

        return wrapper
    return decorator


def no_unicode(argnums=(1,)):
    """
    A decorator that raises a TypeError if any of the given arguments is unicode.

    Example use:

    >>> class bytes(object):
    ...     @no_unicode()
    ...     def __add__(self, other):
    ...          pass

    >>> newbytes(b'1234') + u'1234'     #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    TypeError: argument can't be unicode string
    """
    if isinstance(argnums, int):
        argnums = (argnums,)
    disallowed_types = [unicode] * len(argnums)
    return disallow_types(argnums, disallowed_types)


class newbytes(_builtin_bytes):
    """
    A backport of the Python 3 bytes object to Py2
    """
    def __new__(cls, *args, **kwargs):
        """
        From the Py3 bytes docstring:

        bytes(iterable_of_ints) -> bytes
        bytes(string, encoding[, errors]) -> bytes
        bytes(bytes_or_buffer) -> immutable copy of bytes_or_buffer
        bytes(int) -> bytes object of size given by the parameter initialized with null bytes
        bytes() -> empty bytes object
        
        Construct an immutable array of bytes from:
          - an iterable yielding integers in range(256)
          - a text string encoded using the specified encoding
          - any object implementing the buffer API.
          - an integer
        """
        
        if len(args) == 0:
            return super(newbytes, cls).__new__(cls)
        elif isinstance(args[0], _builtin_bytes):
            value = args[0]
        elif isinstance(args[0], unicode):
            if 'encoding' not in kwargs:
                raise TypeError('unicode string argument without an encoding')
            value = args[0].encode(**kwargs)
        elif isinstance(args[0], Iterable):
            if len(args[0]) == 0:
                # What is this?
                raise ValueError('unknown argument type')
            elif len(args[0]) > 0 and isinstance(args[0][0], int):
                # It's a list of integers
                value = b''.join([chr(x) for x in args[0]])
            else:
                raise ValueError('item cannot be interpreted as an integer')
        elif isinstance(args[0], int):
            if args[0] < 0:
                raise ValueError('negative count')
            value = b'\x00' * args[0]
        else:
            value = args[0]
        return super(newbytes, cls).__new__(cls, value)
        
    def __repr__(self):
        return 'b' + super(newbytes, self).__repr__()

    def __str__(self):
        return 'b' + "'{}'".format(super(newbytes, self).__str__())

    def __getitem__(self, y):
        value = super(newbytes, self).__getitem__(y)
        if isinstance(y, int):
            return ord(value)
        else:
            return newbytes(value)

    def __contains__(self, key):
        if isinstance(key, int):
            newbyteskey = newbytes([key])
        elif isinstance(key, newbytes):
            newbyteskey = key
        else:
            newbyteskey = newbytes(key)
        return issubset(list(newbyteskey), list(self))
    
    @no_unicode()
    def __add__(self, other):
        return newbytes(super(newbytes, self).__add__(other))

    @no_unicode()
    def __radd__(self, left):
        return newbytes(left) + self
            
    def join(self, iterable_of_bytes):
        errmsg = 'sequence item {}: expected bytes, found unicode string'
        for i, item in enumerate(iterable_of_bytes):
            if isinstance(item, unicode):
                raise TypeError(errmsg.format(i))
        return newbytes(super(newbytes, self).join(iterable_of_bytes))

    @classmethod
    def fromhex(cls, string):
        # Only on Py2:
        return cls(string.replace(' ', '').decode('hex'))

    @no_unicode()
    def find(self, sub, *args):
        return newbytes(super(newbytes, self).find(sub, *args))

    @no_unicode()
    def rfind(self, sub, *args):
        return newbytes(super(newbytes, self).rfind(sub, *args))

    @no_unicode((1, 2))
    def replace(self, old, new, *args):
        return newbytes(super(newbytes, self).replace(old, new, *args))

    def encode(self, *args):
        raise AttributeError("encode method has been removed from newbytes")

    @no_unicode(1)
    def startswith(self, prefix, *args):
        return super(newbytes, self).startswith(prefix, *args)

    @no_unicode(1)
    def endswith(self, prefix, *args):
        return super(newbytes, self).endswith(prefix, *args)

    @no_unicode(1)
    def split(self, sep=None, maxsplit=-1):
        return newbytes(super(newbytes, self).split(sep, maxsplit=maxsplit))

    @no_unicode(1)
    def rsplit(self, sep=None, maxsplit=-1):
        return newbytes(super(newbytes, self).rsplit(sep, maxsplit=maxsplit))

    @no_unicode(1)
    def partition(self, sep):
        parts = super(newbytes, self).partition(sep)
        return tuple(newbytes(part) for part in parts)

    @no_unicode(1)
    def rpartition(self, sep):
        parts = super(newbytes, self).rpartition(sep)
        return tuple(newbytes(part) for part in parts)

    @no_unicode(1)
    def index(self, sub, *args):
        '''
        Returns index of sub in bytes.
        Raises ValueError if byte is not in bytes and TypeError if can't
        be converted bytes or its length is not 1.
        '''
        if isinstance(sub, int):
            if len(args) == 0:
                start, end = 0, len(self)
            elif len(args) == 1:
                start = args[0]
            elif len(args) == 2:
                start, end = args
            else:
                raise TypeError('takes at most 3 arguments')
            return list(self)[start:end].index(sub)
        if not isinstance(sub, bytes):
            try:
                sub = self.__class__(sub)
            except (TypeError, ValueError):
                raise TypeError("can't convert sub to bytes")
        try:
            return super(newbytes, self).index(sub, *args)
        except ValueError:
            raise ValueError('substring not found')

# class bytes(_builtin_bytes):
#     '''
#     This class stores bytes data in a similar way to the bytes object in Python
#     3.x.
# 
#     Implemented for python-future to provide a bytes object in Py2 that is
#     better and more consistent with that in Py3.
# 
#     bytes(iterable_of_ints) -> bytes
#     bytes(string, encoding[, errors]) -> bytes
#     bytes(bytes_or_buffer) -> immutable copy of bytes_or_buffer
#     bytes(int) -> bytes object of size given by the parameter initialized with null bytes
#     bytes() -> empty bytes object
#     '''
#     def __init__(self, value, *args, **kwargs):
#         '''
#         Takes an iterable value that should contain either integers in
#         range(256) or corresponding characters.  Some examples for
#         working with bytes:
# 
#         >>> 
#         >>> r = bytes(b'Hello world!')
#         >>> r[0]
#         bytes((0x48))
#         >>> byte_tuple = (115, 101, 99, 114, 101, 116)
#         >>> bytes(byte_tuple) == bytes(b'secret')
#         True
#         >>> bytes(b'Hello world!').toString()
#         String('Hello world!')
#         '''
#         if isinstance(value, bytes):
#             value = value._data
#         else:
#             if isinstance(value, int):
#                 value = (value,)
#             if not (hasattr(value, '__iter__') or hasattr(value, '__getitem__')):
#                 raise TypeError('value must be iterable')
#             if isinstance(value, _builtin_bytes):
#                 # this makes sure that iterating over value gives one byte at a time
#                 # in python 2 and 3
#                 if _builtin_bytes == str:
#                     # in python 2 iterating over bytes gives characters instead of integers
#                     value = tuple(map(ord, value))
#                 else:
#                     # Only tuple-ify if not already tuple-ified by map above
#                     value = tuple(value)
#             elif _builtin_bytes==str and isinstance(value, unicode):
#                 value = tuple(map(ord, value.encode('utf-8')))
#             elif isinstance(value, str):
#                 # only python3 strings here
#                 value = tuple(value.encode('utf-8'))
#             elif isinstance(value, String):
#                 value = value.tobytes()._data
#             else:
#                 # maybe a list of ints?
#                 try:
#                     value = tuple(map(int, value))
#                 except ValueError:
#                     raise ValueError('values must be ints')
# 
#                 for i in value:
#                     if i < 0 or i > 255:
#                         raise ValueError('values not in range(256)')
# 
#         self._data = value
# 
#     def __eq__(self, other):
#         if isinstance(other, self.__class__):
#             return self._data.__eq__(other._data)
#         return NotImplemented
# 
#     def __add__(self, other):
#         if not isinstance(other, self.__class__):        
#             try:
#                 other = self.__class__(other)
#             except (TypeError, ValueError):
#                 return NotImplemented
#         return self.__class__(self._data.__add__(other._data))
#     
#     def __len__(self):
#         return self._data.__len__()
# 
#     def __getitem__(self, key):
#         return self.__class__(self._data.__getitem__(key))
# 
#     def __contains__(self, key):
#         try:
#             key = self.__class__(key)
#         except (TypeError, ValueError):
#             return False
#         if len(key) > 1:
#             return False
#         return self._data.__contains__(key._data[0])
# 
#     def __iter__(self):
#         return self._data.__iter__()
# 
#     def __hash__(self):
#         return self._data.__hash__()
# 
#     def __repr__(self):
#         return 'bytes((' + ','.join(map(hex, self._data)) + '))'
#     
#     def __int__(self):
#         '''
#         Converts the data to an int if it contains exactly one byte.
#         '''
#         if self.__len__() != 1:
#             raise TypeError('must be of length 1')
#         return self._data[0]
#     
#     def index(self, byte):
#         '''
#         Returns index of byte in bytes.
#         Raises ValueError if byte is not in bytes and TypeError if can't be
#         converted bytes or its length is not 1.
#         '''
#         if not isinstance(byte, bytes):
#             try:
#                 byte = self.__class__(byte)
#             except (TypeError, ValueError):
#                 raise TypeError("can't convert byte to bytes")
#         if len(byte) != 1:
#             raise TypeError('byte must be of length 1')
#         try:
#             return self._data.index(byte._data[0])
#         except ValueError:
#             raise ValueError('byte not in bytes')
# 
#     def split(self, byte, maxsplit=-1):
#         '''
#         Splits bytes on every occurrence of byte.
#         '''
#         if (maxsplit == 0):
#             return [self]
#         try:
#             ind = self.index(byte)
#         except ValueError:
#             return [self]
#         return [self.__class__(self._data[:ind])] + self.__class__(self._data[ind+1:]).split(byte, maxsplit-1)
# 
#     def toString(self):
#         return String(self.export().decode('utf-8'))
#     
#     def export(self):
#         '''
#         Returns the data as bytes() so that you can use it for methods that
#         expect bytes. Don't use this for comparison!
#         '''
#         if _builtin_bytes == str:
#             return _oldbytes().join(map(chr,self._data))
#         return _oldbytes(self._data)
# 
#     def repr(self):
#         return _oldbytes().join(map(chr, selfA))
# 
#     # @typecheck_args( Self(), Not(unicode), vargs=Any(), kwargs=Any() )
#     def startswith(self, prefix, *vargs, **kwargs):
#         return super(bytes, self).startswith(prefix, *vargs, **kwargs)


if PY3:
    import builtins
    bytes = builtins.bytes
    __all__ = []
else:
    bytes = newbytes
    __all__ = ['bytes']

