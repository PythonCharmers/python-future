"""
future: clean single-source support for Python 3 and 2
======================================================

The ``future`` module helps run Python 3.x-compatible code under Python 2
with minimal code cruft.

The goal is to allow you to write clean, modern, forward-compatible
Python 3 code today and to run it with minimal effort under Python 2
alongside a Python 2 stack that may contain dependencies that have not
yet been ported to Python 3.

It is designed to be used as follows::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future import standard_library
    from future.builtins import *
    
followed by clean Python 3 code (with a few restrictions) that can run
unchanged on Python 2.7.

After the imports, this code runs identically on Python 3 and 2::
    
    # Support for renamed standard library modules via import hooks
    from http.client import HttpConnection
    from itertools import filterfalse
    from test import support

    # Backported Py3-like bytes object
    b = bytes(b'ABCD')
    assert list(b) == [65, 66, 67, 68]
    assert repr(b) == "b'ABCD'"
    # These raise TypeErrors:
    # b + u'EFGH'
    # bytes(b',').join([u'Fred', u'Bill'])

    # New iterable range object with slicing support
    for i in range(10**15)[:10]:
        pass
    
    # Other iterators: map, zip, filter
    my_iter = zip(range(3), ['a', 'b', 'c'])
    assert my_iter != list(my_iter)
    
    # New simpler super() function:
    class VerboseList(list):
        def append(self, item):
            print('Adding an item')
            super().append(item)
    
    # These raise NameErrors:
    # apply(), cmp(), coerce(), reduce(), xrange(), etc.
    
    # This identity is restored. This is normally valid on Py3 and Py2,
    # but 'from __future__ import unicode_literals' breaks it on Py2:
    assert isinstance('happy', str)
    
    # The round() function behaves as it does in Python 3, using
    # "Banker's Rounding" to the nearest even last digit:
    assert round(0.1250, 2) == 0.12
    
    # input() replaces Py2's raw_input() (with no eval()):
    name = input('What is your name? ')
    print('Hello ' + name)


On Python 3, the import lines have zero effect (and zero namespace
pollution).

On Python 2, ``from future import standard_library`` installs
import hooks to allow renamed and moved standard library modules to be
imported from their new Py3 locations.

On Python 2, the ``from future.builtins import *`` line shadows builtins
to provide their Python 3 semantics. (See below for the explicit import
form.)


Standard library reorganization
-------------------------------
``future`` supports the standard library reorganization (PEP 3108)
via import hooks, allowing almost all moved standard library modules to be
accessed under their Python 3 names and locations in Python 2::
    
    from future import standard_library
    
    import socketserver
    import queue
    import configparser
    import test.support
    from collections import UserList
    from itertools import filterfalse, zip_longest
    # and other moved modules and definitions

It also includes backports for these stdlib packages from Py3 that were
heavily refactored versus Py2::
    
    import html, html.entities, html.parser
    import http, http.client

These currently are not supported, but we may support them in the
future::
    
    import http.server, http.cookies, http.cookiejar
    import urllib, urllib.parse, urllib.request, urllib.error


Utilities
---------
``future`` also provides some useful functions and decorators to ease backward
compatibility with Py2 in the ``future.utils`` module. These are a selection
of the most useful functions from ``six`` and various home-grown Py2/3
compatibility modules from various Python projects, such as Jinja2, Pandas,
IPython, and Django.

Examples::

    # Functions like print() expect __str__ on Py2 to return a byte
    string. This decorator maps the __str__ to __unicode__ on Py2 and
    defines __str__ to encode it as utf-8:

    from future.utils import python_2_unicode_compatible

    @python_2_unicode_compatible
    class MyClass(object):
        def __str__(self):
            return u'Unicode string: \u5b54\u5b50'
    a = MyClass()

    # This then prints the Chinese characters for Confucius:
    print(a)


    # Iterators on Py3 require a __next__() method, whereas on Py2 this
    # is called next(). This decorator allows Py3-style iterators to work
    # identically on Py2:

    @implements_iterator
    class Upper(object):
        def __init__(self, iterable):
            self._iter = iter(iterable)
        def __next__(self):                 # note the Py3 interface
            return next(self._iter).upper()
        def __iter__(self):
            return self

    print(list(Upper('hello')))
    # prints ['H', 'E', 'L', 'L', 'O']

On Python 3 these decorators are no-ops.


Explicit imports
----------------
If you prefer explicit imports, the explicit equivalent of the ``from
future.builtins import *`` line above is::
    
    from future.builtins.iterators import zip, map, filter
    from future.builtins.misc import ascii, oct, hex, chr, input
    from future.builtins.backports import bytes, range, super, round
    from future.builtins.disabled import (apply, cmp, coerce,
            execfile, file, long, raw_input, reduce, reload, unicode,
            xrange, StandardError)
    from future.builtins.str_is_unicode import str

But please note that the API is still evolving rapidly.

See the docstrings for each of these modules for more info::

- future.standard_library
- future.builtins
- future.utils


Automatic conversion
====================
An experimental script called ``futurize`` is included to aid in making
either Python 2 code or Python 3 code compatible with both platforms
using the ``future`` module. See
https://github.com/edschofield/python-future#automatic-conversion.


Credits
=======
:Author:  Ed Schofield
:Sponsor: Python Charmers Pty Ltd, Australia, and Python Charmers Pte
          Ltd, Singapore. http://pythoncharmers.com
:Others:  - ``future`` incorporates the ``six`` module by Benjamin
            Peterson.
          - The ``futurize`` script uses ``lib2to3``, ``lib3to2``, and
            parts of Armin Ronacher's ``python-modernize`` code.
          - The backported ``super()`` and ``range()`` functions are
            derived from Ryan Kelly's ``magicsuper`` module and Dan Crosta's
            ``xrange`` module.
          - The ``python_2_unicode_compatible`` decorator is from
            ``django.utils.encoding``.


Licensing
---------
Copyright 2013 Python Charmers Pty Ltd, Australia.
The software is distributed under an MIT licence. See LICENSE.txt.


FAQ
===
See https://github.com/edschofield/python-future#faq.

"""
# pylint: disable=W0622,W0401

from future import utils
from future.builtins import *

if not utils.PY3:
    # Only shadow builtins on Py2; no new names
    __all__ = ['filter', 'map', 'zip', 
               'ascii', 'oct', 'hex', 'chr', 'int',
               'apply', 'cmp', 'coerce', 'execfile', 'file', 'long',
               'raw_input', 'reduce', 'reload', 'unicode', 'xrange',
               'StandardError',
               'round', 'input', 'range', 'super',
               'str']

else:
    # No namespace pollution on Py3
    __all__ = []

__ver_major__ = 0
__ver_minor__ = 5
__ver_patch__ = 0
__ver_sub__ = ''
__version__ = "%d.%d.%d%s" % (__ver_major__, __ver_minor__,
                              __ver_patch__, __ver_sub__)


