"""
A selection of cross-compatible functions for Python 2 and 3.

These come from several sources:
* Jinja2 (BSD licensed: see https://github.com/mitsuhiko/jinja2/blob/master/LICENSE
* Pandas compatibility module pandas.compat
* six.py by Benjamin Peterson
* Django

This exports useful functions for 2/3 compatible code that are not
builtins on Python 3:
* bind_method: binds functions to classes
* ``native_str_to_bytes`` and ``bytes_to_native_str``
* ``native_str``: always equal to the native platform string object (because
  this may be shadowed by imports from future.builtins)
* lists: lrange(), lmap(), lzip(), lfilter()
* iterable method compatibility: iteritems, iterkeys, itervalues
  * Uses the original method if available, otherwise uses items, keys, values.
* types:
    * text_type: unicode in Python 2, str in Python 3
    * binary_type: str in Python 2, bythes in Python 3
    * string_types: basestring in Python 2, str in Python 3

* bchr(c):
    Take an integer and make a 1-character byte string
* bord(c)
    Take the result of indexing on a byte string and make an integer
* tobytes(s)
    Take a text string, a byte string, or a sequence of characters taken
    from a byte string, and make a byte string.

This module also defines a simple decorator called
``python_2_unicode_compatible`` (from django.utils.encoding) which
defines ``__unicode__`` and ``__str__`` methods consistently under Python
3 and 2. To support Python 3 and 2 with a single code base, simply define
a ``__str__`` method returning unicode text and apply the
python_2_unicode_compatible decorator to the class like this::
    
    >>> from future.utils import python_2_unicode_compatible
    
    >>> @python_2_unicode_compatible
    ... class MyClass(object):
    ...     def __str__(self):
    ...         return u'Unicode string: \u5b54\u5b50'
    
    >>> a = MyClass()

Then, after this import:

    >>> from future.builtins import str
    
the following is ``True`` on both Python 3 and 2::
    
    >>> str(a) == a.encode('utf-8').decode('utf-8')
    True

and, on a Unicode-enabled terminal with the right fonts, these both print the
Chinese characters for Confucius::
    
    print(a)
    print(str(a))

On Python 3, this decorator is a no-op.

"""

import types
import sys
import numbers

PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2
PYPY = hasattr(sys, 'pypy_translation_info')


def python_2_unicode_compatible(cls):
    """
    A decorator that defines __unicode__ and __str__ methods under Python
    2. Under Python 3 it does nothing.
    
    To support Python 2 and 3 with a single code base, define a __str__
    method returning unicode text and apply this decorator to the class.

    The implementation comes from django.utils.encoding.
    """
    if not PY3:
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return cls


def with_metaclass(meta, *bases):
    """
    Function from jinja2/_compat.py. License: BSD.

    Use it like this::
        
        class BaseForm(object):
            pass
        
        class FormType(type):
            pass
        
        class Form(with_metaclass(FormType, BaseForm)):
            pass

    This requires a bit of explanation: the basic idea is to make a
    dummy metaclass for one level of class instantiation that replaces
    itself with the actual metaclass.  Because of internal type checks
    we also need to make sure that we downgrade the custom metaclass
    for one level to something closer to type (that's why __call__ and
    __init__ comes back from type etc.).
    
    This has the advantage over six.with_metaclass of not introducing
    dummy classes into the final MRO.
    """
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})


# Definitions from pandas.compat follow:
if PY3:
    def bchr(s):
        return bytes([s])
    def bstr(s):
        if isinstance(s, str):
            return bytes(s, 'latin-1')
        else:
            return bytes(s)
    def bord(s):
        return s
else:
    # Python 2
    def bchr(s):
        return chr(s)
    def bstr(s):
        return str(s)
    def bord(s):
        return ord(s)

###

if PY3:
    def tobytes(s):
        if isinstance(s, bytes):
            return s
        else:
            if isinstance(s, str):
                return s.encode('latin-1')
            else:
                return bytes(s)
else:
    # Python 2
    def tobytes(s):
        '''
        Encodes to latin-1 (where the first 256 chars are the same as
        ASCII.)
        '''
        if isinstance(s, unicode):
            return s.encode('latin-1')
        else:
            return ''.join(s)

if PY3:
    def native_str_to_bytes(s, encoding='ascii'):
        return s.encode(encoding)

    def bytes_to_native_str(b, encoding='ascii'):
        return b.decode(encoding)
else:
    # Python 2
    def native_str_to_bytes(s, encoding='ascii'):
        return s

    def bytes_to_native_str(b, encoding='ascii'):
        return b


if PY3:
    # list-producing versions of the major Python iterating functions
    def lrange(*args, **kwargs):
        return list(range(*args, **kwargs))

    def lzip(*args, **kwargs):
        return list(zip(*args, **kwargs))

    def lmap(*args, **kwargs):
        return list(map(*args, **kwargs))

    def lfilter(*args, **kwargs):
        return list(filter(*args, **kwargs))
else:
    import __builtin__
    # Python 2-builtin ranges produce lists
    lrange = __builtin__.range
    lzip = __builtin__.zip
    lmap = __builtin__.map
    lfilter = __builtin__.filter


def isidentifier(s, dotted=False):
    '''
    A function equivalent to the str.isidentifier method on Py3
    '''
    if dotted:
        return all(isidentifier(a) for a in s.split('.'))
    if PY3:
        return s.isidentifier()
    else:
        import re
        _name_re = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*$")
        return bool(_name_re.match(s))


def viewitems(obj, **kwargs):
    """
    Function for iterating over dictionary items with the same set-like
    behaviour on Py2.7 as on Py3.

    Passes kwargs to method."""
    func = getattr(obj, "viewitems", None)
    if not func:
        func = obj.items
    return func(**kwargs)


def viewkeys(obj, **kwargs):
    """
    Function for iterating over dictionary keys with the same set-like
    behaviour on Py2.7 as on Py3.

    Passes kwargs to method."""
    func = getattr(obj, "viewkeys", None)
    if not func:
        func = obj.keys
    return func(**kwargs)


def viewvalues(obj, **kwargs):
    """
    Function for iterating over dictionary values with the same set-like
    behaviour on Py2.7 as on Py3.

    Passes kwargs to method."""
    func = getattr(obj, "viewvalues", None)
    if not func:
        func = obj.values
    return func(**kwargs)


def iteritems(obj, **kwargs):
    """Use this only if compatibility with Python versions before 2.7 is
    required. Otherwise, prefer viewitems().
    """
    func = getattr(obj, "iteritems", None)
    if not func:
        func = obj.items
    return func(**kwargs)


def iterkeys(obj, **kwargs):
    """Use this only if compatibility with Python versions before 2.7 is
    required. Otherwise, prefer viewkeys().
    """
    func = getattr(obj, "iterkeys", None)
    if not func:
        func = obj.keys
    return func(**kwargs)


def itervalues(obj, **kwargs):
    """Use this only if compatibility with Python versions before 2.7 is
    required. Otherwise, prefer viewvalues().
    """
    func = getattr(obj, "itervalues", None)
    if not func:
        func = obj.values
    return func(**kwargs)


def bind_method(cls, name, func):
    """Bind a method to class, python 2 and python 3 compatible.

    Parameters
    ----------

    cls : type
        class to receive bound method
    name : basestring
        name of method on class instance
    func : function
        function to be bound as method

    Returns
    -------
    None
    """
    # only python 2 has bound/unbound method issue
    if not PY3:
        setattr(cls, name, types.MethodType(func, None, cls))
    else:
        setattr(cls, name, func)


def getexception():
    return sys.exc_info()[1]


def reraise(tp, value=None, tb=None):
    """
    Create a raise_ method that allows re-raising exceptions with the cls
    value and traceback on Python2 & Python3.
    """
    if PY3:
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
    else:
        exec('def reraise(tp, value=None, tb=None):\n raise tp, value, tb')


def implements_iterator(cls):
    '''
    From jinja2/_compat.py. License: BSD.

    Use as a decorator like this::
        
        @implements_iterator
        class UppercasingIterator(object):
            def __init__(self, iterable):
                self._iter = iter(iterable)
            def __iter__(self):
                return self
            def __next__(self):
                return next(self._iter).upper()
    
    '''
    if PY3:
        return cls
    else:
        cls.next = cls.__next__
        del cls.__next__
        return cls

if PY3:
    get_next = lambda x: x.next
else:
    get_next = lambda x: x.__next__


def encode_filename(filename):
    if PY3:
        return filename
    else:
        if isinstance(filename, unicode):
            return filename.encode('utf-8')
        return filename


def is_new_style(cls):
    """
    Python 2.7 has both new-style and old-style classes. Old-style classes can
    be pesky in some circumstances, such as when using inheritance.  Use this
    function to test for whether a class is new-style. (Python 3 only has
    new-style classes.)
    """
    return hasattr(cls, '__class__') and ('__dict__' in dir(cls) 
                                          or hasattr(cls, '__slots__'))

# The native platform string and bytes types. Useful because ``str`` and
# ``bytes`` are redefined on Py2 by ``from future.builtins import *``.
native_str = str
native_bytes = bytes


def istext(obj):
    """
    Deprecated. Use::
        >>> isinstance(obj, str)
    after this import:
        >>> from future.builtins import str
    """
    return isinstance(obj, type(u''))


def isbytes(obj):
    """
    Deprecated. Use::
        >>> isinstance(obj, bytes)
    after this import:
        >>> from future.builtins import bytes
    """
    return isinstance(obj, type(b''))


def isnewbytes(obj):
    """
    Equivalent to the result of ``isinstance(obj, newbytes)`` were
    ``__instancecheck__`` not overridden on the newbytes subclass. In
    other words, it is REALLY a newbytes instance, not a Py2 native str
    object?
    """
    # TODO: generalize this so that it works with subclasses of newbytes
    # Import is here to avoid circular imports:
    from future.builtins.backports.newbytes import newbytes
    return type(obj) == newbytes


def isint(obj):
    """
    Deprecated. Tests whether an object is a Py3 ``int`` or either a Py2 ``int`` or
    ``long``.

    Instead of using this function, you can use:

        >>> from future.builtins import int
        >>> isinstance(obj, int)

    The following idiom is equivalent:

        >>> from numbers import Integral
        >>> isinstance(obj, Integral)
    """

    return isinstance(obj, numbers.Integral)


def native(obj):
    """
    On Py3, this is a no-op: native(obj) -> obj

    On Py2, returns the corresponding native Py2 types that are
    superclasses for backported objects from Py3:
    
    >>> from future.builtins import str, bytes, int

    >>> native(str(u'ABC'))
    u'ABC'
    >>> type(native(str(u'ABC')))
    unicode

    >>> native(bytes(b'ABC'))
    b'ABC'
    >>> type(native(bytes(b'ABC')))
    bytes

    >>> native(int(10**20))
    100000000000000000000L
    >>> type(native(int(10**20)))
    long

    Existing native types on Py2 will be returned unchanged:

    >>> type(native(u'ABC'))
    unicode
    """
    if hasattr(obj, '__native__'):
        return obj.__native__()
    else:
        return obj


def old_div(a, b):
    """
    Equivalent to ``a / b`` on Python 2 without ``from __future__ import
    division``.
    """
    return a // b if (isint(a) and isint(b)) else a / b


__all__ = ['PY3', 'PY2', 'PYPY', 'python_2_unicode_compatible',
           'with_metaclass', 'bchr', 'bstr', 'bord',
           'tobytes', 'str_to_native_bytes', 'bytes_to_native_str', 
           'lrange', 'lmap', 'lzip', 'lfilter',
           'isidentifier', 'iteritems', 'iterkeys', 'itervalues',
           'viewitems', 'viewkeys', 'viewvalues',
           'bind_method', 'getexception',
           'reraise', 'implements_iterator', 'get_next', 'encode_filename',
           'is_new_style', 'native_str']

