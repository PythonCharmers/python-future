"""
Tools for hacking the builtin types
"""
import ctypes as c
from contextlib import contextmanager


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

def hackclass(class_, name):
    """Decorator to add decorated method named `name` the class
    `class_`. So you can use it like this:

        >>> @hackclass(dict, 'banner')
        ... def dict_banner(self):
        ...     l = len(self)
        ...     print('This dict has {0} element{1}'.format(
        ...         l, l is 1 and '' or 's')
        >>> {'a': 1, 'b': 2}.banner()
        'This dict has 2 elements'
    """
    def wrapper(func):
        get_dict(class_)[name] = func
        return func
    return wrapper

@contextmanager
def hackclass_context(class_, name, func):
    # import pdb
    # pdb.set_trace()
    oldmethod = None
    if hasattr(class_, name):
        oldmethod = getattr(class_, name)
    if func is not None:
        get_dict(class_)[name] = func
    else:
        try:
            del get_dict(class_)[name]
        except KeyError:
            pass

    yield

    if oldmethod is None:
        try:
            del get_dict(class_)[name]
        except KeyError:
            pass
    else:
        get_dict(class_)[name] = oldmethod

