.. _quickstart-guide:

Quick-start guide
=================

The ``future`` module helps run Python 3.x-compatible code under Python 2
with minimal code cruft.

You can use it to help to port your code from Python 2 to Python 3 today -- and
still have it run on Python 2.

If you already have Python 3 code, you can also use ``future`` to offer Python 2
compatibility with almost no extra work.


If you are writing code from scratch
------------------------------------

Start each module with these lines::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future import standard_library
    from future.builtins import *

Then write standard Python 3 code. The ``future`` package will provide support
for running your code on Python 2 mostly unchanged.


To convert existing Python 2 code
---------------------------------

If you already know Python 3, start with the :ref:`automatic-conversion` page.
If you don't know Python 3 yet, start with :ref:`python3-essentials`.


To convert existing Python 3 code
---------------------------------

To offer backward compatibility with Python 2, simply add these lines
at the top of your Python 3 modules::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future import standard_library
    from future.builtins import *
    
Then most Python 3 code should simply work on Python 2.

There are some things to be aware of, however: see :ref:`backwards-conversion`.


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

``future`` also includes backports for these stdlib packages from Py3 that were
heavily refactored versus Py2::
    
    import html, html.entities, html.parser
    import http, http.client, http.server

These modules are currently not supported, but we aim to support them in the
future::
    
    import http.cookies, http.cookiejar
    import urllib, urllib.parse, urllib.request, urllib.error


For more information, see :ref:`standard-library`.


For examples of code fragments that run identically on Python 3 and 2, see
:ref:`code-examples`.

For a more substantial example, you can see the included `backported http.client module
<https://github.com/edschofield/python-future/blob/master/future/standard_library/http/client.py>`_,
but be warned: there is not much to see. It is mostly the same as the Python
3.3 standard library code.
    

.. _utilities-guide:
Utilities
---------

``future`` also provides some useful functions and decorators to ease backward
compatibility with Py2 in the ``future.utils`` module. These are a selection
of the most useful functions from ``six`` and various home-grown Py2/3
compatibility modules from various Python projects, such as Jinja2, Pandas,
IPython, and Django.

Examples::

    # Functions like print() expect __str__ on Py2 to return a byte
    # string. This decorator maps the __str__ to __unicode__ on Py2 and
    # defines __str__ to encode it as utf-8:

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


For more information, see :ref:`what-else`.

