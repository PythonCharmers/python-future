"""
This module redefines ``str`` on Python 2.x to be the unicode type and
provides a decorator called ``python_2_unicode_compatible`` to be applied to
classes.

It is designed to be used together with the ``unicode_literals`` import as
follows:

    >>> from __future__ import unicode_literals
    >>> from future.builtins.str_is_unicode import str

On Python 3.x and normally on Python 2.x, these expressions hold

    >>> str('blah') is 'blah'
    True
    >>> isinstance('blah', str)
    True

However, on Python 2.x, with this import:

    >>> from __future__ import unicode_literals

the same expressions are False:

    >>> str('blah') is 'blah'
    False
    >>> isinstance('blah', str)
    False

This module is designed to be imported together with unicode_literals on
Python 2 to bring the meaning of ``str`` back into alignment with
unprefixed string literals (i.e. ``unicode`` if ``unicode_literals`` has
been imported from ``__future__``).

Note that ``str()`` (and ``print()``) would then normally call the
``__unicode__`` method on objects in Python 2. To define string
representations of your objects portably across Py3 and Py2, use::
    
    >>> from future.utils import python_2_unicode_compatible
    
    >>> @python_2_unicode_compatible
    ... class MyClass(object):
    ...     def __str__(self):
    ...         return u'Unicode string: \u5b54\u5b50'
    
    >>> a = MyClass()

Then, for example, the following is true on both Python 3 and 2::
    
    >>> str(a) == a.encode('utf-8').decode('utf-8')
    True

On a Unicode-enabled terminal with the right fonts, these both then print
the Chinese characters for Confucius::
    
    print(a)
    print(str(a))

On Python 3, the python_2_unicode_compatible decorator is a no-op.

"""

from future import utils

if not utils.PY3:
    str = unicode
    __all__ = ['str']
else:
    import builtins
    str = builtins.str
    __all__ = []
