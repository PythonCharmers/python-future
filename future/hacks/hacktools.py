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


def dispatch_methods(cls, smethods):
    """
    Pass in special methods names to graft onto a class.

    E.g. dispatch_methods(MyClass, ['__repr__', '__str__'])
    """
    # Treat smethods like a list of strings unless it's a string:
    if isinstance(smethods, basestring):
        smethods = [smethods]
    for sm in smethods:
        def closure(self, *args, **kwargs):
            return self.__dict__[sm](*args, **kwargs)
        try:
            setattr(cls, sm, closure)
        except TypeError as e:
            if not 'built-in/extension type' in e.message:
                raise e
            get_dict(cls)[sm] = closure

def hack_special_method(cls, newmethodname, newmethod):
    """
    This works on user-defined classes but apparently not with
    builtin objects like bytes.

    Example:
        
        >>> class A(object);
        ...     def __repr__(self):
        ...         return 'old repr'
        >>> a = A()
        >>> hack_special_method(A, '__repr__',
                                lambda self: 'new repr')
        >>> a
        'new repr'
        >>> b = A()
        >>> b
        'new repr'
    """

    dispatch_methods(cls, [newmethodname])
    get_dict(cls)[newmethodname] = newmethod

    
#     [newmethodname] = 
# def move_to_instance_dict(cls, local_dict=None):
#     """
#     Move local definitions to an instance dictionary of the given class.
#     Based on Raymond Hettinger's recipe here:
#         http://code.activestate.com/recipes/578091/
#     """
#     o = cls()
#     if local_dict is None:
#         local_dict = sys._getframe(1).f_locals
#     vars(o).update(local_dict)
#     return o
