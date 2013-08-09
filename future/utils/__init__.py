"""
This module defines a simple decorator called python_2_unicode_compatible
(borrowed from django.utils.encoding) which defines ``__unicode__`` and
``__str__`` methods consistently under Python 3 and 2. To support Python
3 and 2 with a single code base, simply define a ``__str__`` method
returning unicode text and apply the python_2_unicode_compatible
decorator to the class like this::
    
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

from future import six


def python_2_unicode_compatible(klass):
    """
    A decorator that defines __unicode__ and __str__ methods under Python
    2. Under Python 3 it does nothing.
    
    To support Python 2 and 3 with a single code base, define a __str__
    method returning text and apply this decorator to the class.

    The implementation comes from django.utils.encoding.
    """
    if not six.PY3:
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return klass

