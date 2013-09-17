"""
Uses the Forbidden Fruit package to hack the builtin bytes type
"""

from contextlib import contextmanager
from functools import wraps

from forbiddenfruit import curses, curse, reverse

from future import utils

def require_unicode_arg2(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not isinstance(args[1], unicode):
            raise TypeError('must be unicode, not bytes')
        return f(*args, **kwargs)
    return wrapped

@require_unicode_arg2
def fromhex(self, string):
    return b'\xff\xff'

def myrepr(self):
    print('Calling fancy fn!')
    return b'b' + self.__oldrepr__()

curse(bytes, "__repr__", myrepr)
print(repr(b''))

@contextmanager
def new_bytes_context():
    curse(bytes, "__oldrepr__", bytes.__repr__)
    curse(bytes, "_c___repr", myrepr)
    curse(bytes, "fromhex", classmethod(fromhex))
    yield
    reverse(bytes, "fromhex")
    reverse(bytes, "_c___repr")
    reverse(bytes, "__oldrepr__")

with new_bytes_context():
    b = b'Byte string'
    print(repr(b.fromhex(u'aa 0f')))
    print(repr(bytes.fromhex(u'b3 2e')))

__all__ = ['new_bytes_context']
