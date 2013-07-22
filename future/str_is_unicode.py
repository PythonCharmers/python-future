"""
This module redefines str on Python 2.x to be the unicode type and
provides a decorator called python_2_unicode_compatible to be applied to
classes.

It is designed to be used together with the unicode_literals import as
follows:

    from __future__ import unicode_literals
    from future import str_is_unicode

On Python 3.x and normally on Python 2.x, this expression:

    str('blah') is 'blah'

return True.

However, on Python 2.x, with this import:

    from __future__ import unicode_literals

the same expression

    str('blah') is 'blah'

returns False.

This module is designed to be imported together with unicode_literals on
Python 2 to bring the meaning of str() back into alignment with
unprefixed string literals.

Note that str() would then normally call the __unicode__ method on
objects in Python 2. Therefore this module also defines a simple
decorator called python_2_unicode_compatible (borrowed from
django.utils.encoding) which defines __unicode__ and __str__ methods
under Python 2. To support Python 2 and 3 with a single code base, simply
define a __str__ method returning text and apply the
python_2_unicode_compatible decorator to the class like this:::

    from future import str_is_unicode

    @python_2_unicode_compatible
    class MyClass(object):
        def __str__(self):
            return u'Unicode string: \u5b54\u5b50'

    a = MyClass()

Then this is True on both Python 3 and 2:::

    str(a) == bytes(a).decode('utf-8')

and, on a Unicode-enabled terminal with the right fonts, these both print
the Chinese name of Confucius:::

    print(a)
    print(str(a))

"""

from __future__ import unicode_literals

import inspect
import imp
import logging

from . import six


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


if not six.PY3:
    caller = inspect.currentframe().f_back
    caller.f_globals['str'] = unicode

