.. _quickstart-guide:

Quick-start guide
=================

You can use ``future`` to help to port your code from Python 2 to Python 3
today -- and still have it run on Python 2.

If you already have Python 3 code, you can instead use ``future`` to
offer Python 2 compatibility with almost no extra work.

Installation
------------

To install the latest stable version, type::

    pip install future

If you would prefer the latest development version, it is available `here <https://github.com/PythonCharmers/python-future>`_.


If you are writing code from scratch
------------------------------------

The easiest way is to start each new module with these lines::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future.builtins import *

Then write standard Python 3 code. The :mod:`future` package will
provide support for running your code on Python 2.6 and 2.7 mostly unchanged.

See :ref:`what-else` for more details.


To convert existing Python 3 code
---------------------------------

To offer backward compatibility with Python 2 from your Python 3 code,
you can use the ``pasteurize`` script. This adds these lines at the top of each
module::

    from __future__ import absolute_import
    from __future__ import division
    from __future__ import print_function
    from __future__ import unicode_literals
    from future.builtins import open
    from future.builtins import str
    from past.utils import div
    # etc., as needed
    
and converts a few Python 3-only constructs to a form compatible with
both Py3 and Py2. Most remaining Python 3 code should simply work on
Python 2.

See :ref:`backwards-conversion` for more details.


To convert existing Python 2 code
---------------------------------

Start with the :ref:`automatic-conversion` page.

.. If you already know Python 3, start with the :ref:`automatic-conversion` page.
.. If you don't know Python 3 yet, start with :ref:`python3-essentials`.


.. _standard-library:

Standard library reorganization
-------------------------------

:mod:`future` supports the standard library reorganization (PEP 3108)
via import hooks, allowing almost all moved standard library modules to
be accessed under their Python 3 names and locations in Python 2::
    
    from future import standard_library
    with standard_library.hooks():
        import socketserver
        import queue
        import configparser
        import test.support
        import html.parser
        from collections import UserList
        from itertools import filterfalse, zip_longest
        from http.client import HttpConnection
        # and other moved modules and definitions

:mod:`future` also includes backports for these stdlib modules from Py3
that were heavily refactored versus Py2::
    
    import html
    import html.entities
    import html.parser

    import http
    import http.client
    import http.server

The following modules are currently not supported, but we aim to support them in
the future::
    
    import http.cookies
    import http.cookiejar

    import urllib
    import urllib.parse
    import urllib.request
    import urllib.error

    import xmlrpc.client
    import xmlrpc.server

If you need one of these, please open an issue `here
<https://github.com/PythonCharmers/python-future>`_.

For other forms of imports from the standard library, see
:ref:`standard-library-imports`.

For more information on interfaces that have changed in the standard library
between Python 2 and Python 3, see :ref:`stdlib-incompatibilities`.


.. _py2-dependencies:

Python 2-only dependencies
--------------------------

If you have dependencies that support only Python 2, you may be able to use the
``past`` module to automatically translate these Python 2 modules to Python 3
upon import. First, install the Python 2-only package into your Python 3
environment::

    $ pip3 install mypackagename --no-compile   # to ignore SyntaxErrors
    
(or use ``pip`` if this points to your Py3 environment.)

Then add the following code at the top of your (Py3 or Py2/3-compatible)
code::

    from past import autotranslate
    autotranslate('mypackagename')
    import mypackagename

This feature is experimental, and we would appreciate your feedback on
how well this works or doesn't work for you. Please file an issue `here
<https://github.com/PythonCharmers/python-future>`_ or post to the
`python-porting <https://mail.python.org/mailman/listinfo/python-porting>`_
mailing list.

For more information, see :ref:`translation`.

.. _utilities-guide:

Utilities
---------

:mod:`future` also provides some useful functions and decorators to ease
backward compatibility with Py2 in the :mod:`future.utils` and
:mod:`past.utils` modules. These are a selection of the most useful functions
from ``six`` and various home-grown Py2/3 compatibility modules from popular
Python projects, such as Jinja2, Pandas, IPython, and Django. The goal is to
consolidate these in one place, tested and documented, obviating the need for
every project to repeat this work.

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

