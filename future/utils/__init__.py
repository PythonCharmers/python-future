"""
A selection of cross-compatible functions for Python 2 and 3.

These come from several sources:
* six.py by Benjamin Peterson
* Pandas compatibility module pandas.compat
* Django

This exports useful functions for 2/3 compatible code that are not
builtins on Python 3:
* lists: lrange(), lmap(), lzip(), lfilter()
* iterable method compatibility: iteritems, iterkeys, itervalues
  * Uses the original method if available, otherwise uses items, keys, values.
* types:
    * text_type: unicode in Python 2, str in Python 3
    * binary_type: str in Python 2, bythes in Python 3
    * string_types: basestring in Python 2, str in Python 3
* bind_method: binds functions to classes

Python 2.6 compatibility:
* OrderedDict
* Counter

Other items:
* OrderedDefaultDict

This module also defines a simple decorator called
``python_2_unicode_compatible`` (from django.utils.encoding) which
defines ``__unicode__`` and ``__str__`` methods consistently under Python
3 and 2. To support Python 3 and 2 with a single code base, simply define
a ``__str__`` method returning unicode text and apply the
python_2_unicode_compatible decorator to the class like this::
    
    from future.utils import python_2_unicode_compatible
    
    @python_2_unicode_compatible
    class MyClass(object):
        def __str__(self):
            return u'Unicode string: \u5b54\u5b50'
    
    a = MyClass()

Then, after this import:
    from future.builtins.str_is_unicode import str
    
the following is ``True`` on both Python 3 and 2::
    
    str(a) == a.encode('utf-8').decode('utf-8')

and, on a Unicode-enabled terminal with the right fonts, these both print the
Chinese characters for Confucius::
    
    print(a)
    print(str(a))

On Python 3, this decorator is a no-op.
"""

from __future__ import unicode_literals

import sys

PY3 = sys.version_info[0] == 3


def python_2_unicode_compatible(klass):
    """
    A decorator that defines __unicode__ and __str__ methods under Python
    2. Under Python 3 it does nothing.
    
    To support Python 2 and 3 with a single code base, define a __str__
    method returning text and apply this decorator to the class.

    The implementation comes from django.utils.encoding.
    """
    if not PY3:
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return klass

# Definitions from six.py follow:

def with_metaclass(meta, base=object):
    """Create a base class with a metaclass."""
    return meta("NewBase", (base,), {})

# Definitions from pandas.compat follow:
if PY3:
    def isidentifier(s):
        return s.isidentifier()

    def str_to_bytes(s, encoding='ascii'):
        return s.encode(encoding)

    def bytes_to_str(b, encoding='utf-8'):
        return b.decode(encoding)

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
    # Python 2
    import re
    _name_re = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*$")

    def isidentifier(s, dotted=False):
        return bool(_name_re.match(s))

    def str_to_bytes(s, encoding='ascii'):
        return s

    def bytes_to_str(b, encoding='ascii'):
        return b

    import __builtin__
    # Python 2-builtin ranges produce lists
    lrange = __builtin__.range
    lzip = __builtin__.zip
    lmap = __builtin__.map
    lfilter = __builtin__.filter


def iteritems(obj, **kwargs):
    """replacement for six's iteritems for Python2/3 compat
       uses 'iteritems' if available and otherwise uses 'items'.

       Passes kwargs to method."""
    func = getattr(obj, "iteritems", None)
    if not func:
        func = obj.items
    return func(**kwargs)


def iterkeys(obj, **kwargs):
    func = getattr(obj, "iterkeys", None)
    if not func:
        func = obj.keys
    return func(**kwargs)


def itervalues(obj, **kwargs):
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


