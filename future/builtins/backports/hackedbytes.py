import ctypes as c
from contextlib import contextmanager

from future import utils


class PyObject_HEAD(c.Structure):
    _fields_ = [
        ('HEAD', c.c_ubyte * (object.__basicsize__ -
                              c.sizeof(c.c_void_p))),
        ('ob_type', c.c_void_p)
    ]

_get_dict = c.pythonapi._PyObject_GetDictPtr
_get_dict.restype = c.POINTER(c.py_object)
_get_dict.argtypes = [c.py_object]

def get_dict(object):
    return _get_dict(object).contents.value

def hackclass(klass, name):
    """Decorator to add decorated method named `name` the class
    `klass`. So you can use it like this:

        >>> @hackclass(dict, 'banner')
        ... def dict_banner(self):
        ...     l = len(self)
        ...     print('This dict has {0} element{1}'.format(
        ...         l, l is 1 and '' or 's')
        >>> {'a': 1, 'b': 2}.banner()
        'This dict has 2 elements'
    """
    def wrapper(func):
        get_dict(klass)[name] = func
        return func
    return wrapper

@contextmanager
def hackclass_context(klass, name, func):
    # import pdb
    # pdb.set_trace()
    oldmethod = None
    if hasattr(klass, name):
        oldmethod = getattr(klass, name)
    if func is not None:
        get_dict(klass)[name] = func
    else:
        try:
            del get_dict(klass)[name]
        except KeyError:
            pass
    yield
    if oldmethod is None:
        try:
            del get_dict(klass)[name]
        except KeyError:
            pass
    else:
        get_dict(klass)[name] = oldmethod


@hackclass(bytes, 'fromhex')
def fromhex(*args):
    assert len(args) <= 2
    if len(args) == 0:
        raise TypeError('fromhex() takes exactly 1 argument (0 given)')
    string = args[-1]
    return string.replace(' ', '').decode('hex')
    # return b'\xff\xff'
# get_dict(bytes)['fromhex'] = fromhex

oldrepr = get_dict(bytes)['__repr__']

@hackclass(bytes, '__repr__')
def repr(self):
    return b'b' + oldrepr(self)

print(repr(b''.fromhex('aa 0f')))
print(repr(bytes.fromhex('b3 2e')))

# import pdb
# pdb.set_trace()

if not utils.PY3:
    def repr(self):
        return b'b' + self.__oldrepr__()
    get_dict(bytes)['__oldrepr__'] = get_dict(bytes)['__repr__']
    get_dict(bytes)['__repr__'] = repr
    # del get_dict(unicode)['decode']

with hackclass_context(unicode, 'decode', lambda x: 1):
    print(unicode(b'blah'))
    print(u'abc'.decode('utf-8'))

