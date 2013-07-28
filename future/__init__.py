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
    from future import *
    
followed by clean Python 3 code (with a few restrictions) that can run
unchanged on Python 2.7.

On Python 3, the ``from future import *`` line has no effect (i.e. zero
namespace pollution.) On Python 2 it shadows builtins to provide the
Python 3 semantics. (See below for the explicit import form.)

After the imports, this code runs identically on Python 3 and 2::
    
    # New iterable range object with slicing support
    for i in range(10**11)[:10]:
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


``future`` also supports the standard library reorganization (PEP 3108)
via import hooks, allowing standard library modules to be accessed under
their Python 3 names and locations::
    
    from future import standard_library_renames
    
    import socketserver
    import queue
    import configparser
    # and other moved modules

It also includes experimental backports for three stdlib packages from Py3
that were heavily refactored versus Py2::
    
    import urllib, urllib.parse, urllib.request, urllib.error
    import http, http.server, http.client, http.cookies, http.cookiejar
    import html, html.entities, html.parser

Backporting all three packages took about 1 hour using ``future`` itself.
*Warning*: at least ``http.client`` doesn't pass tests yet, since it
depends on a Py3.2+ stdlib feature (``ssl.SSLContext``) that is not
available in Py2.


Explicit imports
----------------
If you prefer explicit imports, the explicit equivalent of the ``from
future import *`` line above is::
    
    from future.common_iterators import zip, map, filter
    from future.builtins import ascii, oct, hex, chr, int
    from future.modified_builtins import (range, super, round, input)
    from future.disable_obsolete_builtins import (apply, cmp, coerce,
            execfile, file, long, raw_input, reduce, reload, unicode,
            xrange, StandardError)
    from future.str_is_unicode import str

But please note that the API is still evolving rapidly.

See the docstrings for each of these modules for more info::

- future.standard_library_renames
- future.common_iterators
- future.builtins
- future.modified_builtins
- future.disable_obsolete_builtins
- future.str_as_unicode


Credits
-------
:Author:  Ed Schofield
:Sponsor: Python Charmers Pty Ltd, Australia, and Python Charmers Pte
          Ltd, Singapore. http://pythoncharmers.com
:Others:  The ``super()`` and ``range()`` functions are derived from Ryan
          Kelly's ``magicsuper`` module and Dan Crosta's ``xrange``
          module. The ``python_2_unicode_compatible`` decorator is from
          ``django.utils.encoding``. The ``fix_metaclass`` 2to3 fixer
          (from Armin Ronacher's ``python-modernize``) was authored by
          Jack Diederich and Daniel Neuhaeuser.


Licensing
---------
Copyright 2013 Python Charmers Pty Ltd, Australia.
The software is distributed under an MIT licence. See LICENSE.txt.


FAQ
---
See https://github.com/edschofield/python-future#faq.

"""

from __future__ import (division, absolute_import, print_function)

from future import six

from future.common_iterators import (filter, map, zip)
from future.builtins import (ascii, oct, hex, chr, int)
from future.modified_builtins import (round, input, range, super)
from future.str_is_unicode import str  

# We don't import the python_2_unicode_compatible decorator; only names
# that shadow the builtins on Py2.

if not six.PY3:
    from future.disable_obsolete_builtins import (apply, cmp, coerce,
            execfile, file, long, raw_input, reduce, reload, unicode,
            xrange, StandardError)
    
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
__ver_minor__ = 3
__ver_patch__ = 0
__ver_sub__ = '-rc2'
__version__ = "%d.%d.%d%s" % (__ver_major__,__ver_minor__,__ver_patch__,__ver_sub__)


