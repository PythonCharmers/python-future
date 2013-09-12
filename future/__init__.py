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

    from __future__ import (division, absolute_import, print_function,
                            unicode_literals)
    from future import standard_library
    from future.builtins import *
    
followed by clean Python 3 code (with a few restrictions) that can run
unchanged on Python 2.7.

On Python 3, ``from future import standard_library`` has no effect. On
Python 2, it module installs import hooks to allow renamed and moved
standard library modules to be imported from their new Py3 locations.

Likewise, on Python 3, the ``from future.builtins import *`` line has no
effect (i.e. zero namespace pollution.) On Python 2 it shadows builtins
to provide their Python 3 semantics. (See below for the explicit import
form.)

After the imports, this code runs identically on Python 3 and 2::
    
    # Support for renamed standard library modules (see below)
    from http.client import HttpConnection
    from itertools import filterfalse
    from test import support

    # New iterable range object with slicing support
    for i in range(10**15)[:10]:
        pass
    
    # Other common iterators: map, reduce, zip
    my_iter = zip(range(3), ['a', 'b', 'c'])
    assert my_iter != list(my_iter)
    
    # New simpler super() function:
    class VerboseList(list):
        def append(self, item):
            print('Adding an item')
            super().append(item)
    
    # These raise NameErrors:
    # apply(), cmp(), coerce(), reduce(), xrange(), etc.
    
    # This identity is restored. This is normally valid on Py3 and Py2, but
    # 'from __future__ import unicode_literals' breaks it on Py2:
    assert isinstance('happy', str)
    
    # The round() function behaves as it does in Python 3, using "Banker's
    # Rounding" to the nearest even last digit:
    assert round(0.1250, 2) == 0.12
    
    # input() is now safe (no eval()):
    name = input('What is your name? ')
    print('Hello ' + name)


Standard library reorganization
-------------------------------
``future`` supports the standard library reorganization (PEP 3108)
via import hooks, allowing almost all moved standard library modules to be
accessed under their Python 3 names and locations::
    
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


Explicit imports
----------------
If you prefer explicit imports, the explicit equivalent of the ``from
future.builtins import *`` line above is::
    
    from future.builtins.iterators import zip, map, filter
    from future.builtins.misc import ascii, oct, hex, chr, input
    from future.builtins.backports import range, super, round
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
A script called ``futurize`` is included to aid in making either Python 2
code or Python 3 code compatible with both platforms using the ``future``
module. See
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
__ver_minor__ = 4
__ver_patch__ = 1
__ver_sub__ = ''
__version__ = "%d.%d.%d%s" % (__ver_major__,__ver_minor__,__ver_patch__,__ver_sub__)


