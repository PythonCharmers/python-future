.. _overview:

Overview: an easier, safer, cleaner upgrade path to Python 3
============================================================


``python-future`` is the missing compatibility layer between Python 3 and
Python 2. It allows you to maintain a single, clean Python 3.x-compatible
codebase with minimal cruft and run it easily on Python 2 mostly unchanged.

It provides ``future`` and ``past`` packages with backports and forward ports of
features from Python 3 and 2. It also comes with ``futurize`` and
``pasteurize``, customized 2to3-based scripts that helps you to convert either
Py2 or Py3 code easily to support both Python 2 and 3 in a single clean
Py3-style codebase, module by module.

Notable projects that use ``future`` for Python 3/2 compatibility are `Mezzanine
<http://mezzanine.jupo.org/>`_ and `ObsPy <http://obspy.org>`_.

.. _features:

Features
--------

-   ``future.builtins`` package provides backports and remappings for 19
    builtins with different semantics on Py3 versus Py2

-   ``future.standard_library`` package provides backports from the Py3.3
    standard library

-   ``future.moves`` package provides support for reorganized standard library
    modules (renames from native packages)

-   ``past.builtins`` package provides forward-ports of Python 2 types and
    resurrects some Python 2 builtins (to aid with per-module code migrations)

-   ``past.translation`` package supports transparent translation of Python 2
    modules to Python 3 upon import. [This feature is currently in alpha.] 

-   800+ unit tests, including many from the Py3.3 source tree.

-   ``futurize`` and ``pasteurize`` scripts based on ``2to3`` and parts of
    ``3to2`` and ``python-modernize``, for automatic conversion from either Py2
    or Py3 to a clean single-source codebase compatible with Python 2.6+ and
    Python 3.3+.

-   a curated set of utility functions and decorators in ``future.utils`` and
    ``past.utils`` selected from Py2/3 compatibility interfaces from projects
    like ``six``, ``IPython``, ``Jinja2``, ``Django``, and ``Pandas``.


.. _code-examples:

Code examples
-------------

Replacements for Py2's built-in functions and types are designed to be imported
at the top of each Python module together with Python's built-in ``__future__``
statements. For example, this code behaves identically on Python 2.6/2.7 after
these imports as it does on Python 3.3+:

.. code-block:: python
    
    from __future__ import absolute_import, division, print_function
    from future.builtins import (bytes, str, open, super, range,
                                 zip, round, input, int, pow, object)

    # Backported Py3 bytes object
    b = bytes(b'ABCD')
    assert list(b) == [65, 66, 67, 68]
    assert repr(b) == "b'ABCD'"
    # These raise TypeErrors:
    # b + u'EFGH'
    # bytes(b',').join([u'Fred', u'Bill'])

    # Backported Py3 str object
    s = str(u'ABCD')
    assert s != bytes(b'ABCD')
    assert isinstance(s.encode('utf-8'), bytes)
    assert isinstance(b.decode('utf-8'), str)
    assert repr(s) == "'ABCD'"      # consistent repr with Py3 (no u prefix)
    # These raise TypeErrors:
    # bytes(b'B') in s
    # s.find(bytes(b'A'))

    # Extra arguments for the open() function
    f = open('japanese.txt', encoding='utf-8', errors='replace')
    
    # New simpler super() function:
    class VerboseList(list):
        def append(self, item):
            print('Adding an item')
            super().append(item)

    # New iterable range object with slicing support
    for i in range(10**15)[:10]:
        pass
    
    # Other iterators: map, zip, filter
    my_iter = zip(range(3), ['a', 'b', 'c'])
    assert my_iter != list(my_iter)
    
    # The round() function behaves as it does in Python 3, using
    # "Banker's Rounding" to the nearest even last digit:
    assert round(0.1250, 2) == 0.12
    
    # input() replaces Py2's raw_input() (with no eval()):
    name = input('What is your name? ')
    print('Hello ' + name)

    # Compatible output from isinstance() across Py2/3:
    assert isinstance(2**64, int)        # long integers
    assert isinstance(u'blah', str)
    assert isinstance('blah', str)       # only if unicode_literals is in effect

    # pow() supports fractional exponents of negative numbers like in Py3:
    z = pow(-1, 0.5)

    # Py3-style iterators written as new-style classes (subclasses of
    # future.builtins.object) are backward compatibile with Py2:
    class Upper(object):
        def __init__(self, iterable):
            self._iter = iter(iterable)
        def __next__(self):                 # note the Py3 interface
            return next(self._iter).upper()
        def __iter__(self):
            return self
    assert list(Upper('hello')) == list('HELLO')


There is also support for renamed standard library modules in the form of import
hooks. The context-manager form works like this:

.. code-block:: python

    from future import standard_library

    with standard_library.hooks():
        from http.client import HttpConnection
        from itertools import filterfalse
        import html.parser
        import queue
        from urllib.request import urlopen


Automatic conversion to Py2/3-compatible code
=============================================

``future`` comes with two scripts called ``futurize`` and
``pasteurize`` to aid in making Python 2 code or Python 3 code compatible with
both platforms (Py2&3). It is based on 2to3 and uses fixers from ``lib2to3``,
``lib3to2``, and ``python-modernize``, as well as custom fixers.

``futurize`` passes Python 2 code through all the appropriate fixers to turn it
into valid Python 3 code, and then adds ``__future__`` and ``future`` package
imports so that it also runs under Python 2.

For conversions from Python 3 code to Py2/3, use the ``pasteurize`` script
instead. This converts Py3-only constructs (e.g. new metaclass syntax) to
Py2/3 compatible constructs and adds ``__future__`` and ``future`` imports to
the top of each module.

In both cases, the result should be relatively clean Py3-style code that runs
mostly unchanged on both Python 2 and Python 3.

.. _forwards-conversion:

Futurize: 2 to both
--------------------

For example, running ``futurize -w mymodule.py`` turns this Python 2 code:

.. code-block:: python
    
    import ConfigParser

    class Blah(object):
        pass
    print 'Hello',

into this code which runs on both Py2 and Py3:

.. code-block:: python
    
    from __future__ import print_function
    from future import standard_library
    
    import configparser

    class Blah(object):
        pass
    print('Hello', end=' ')

For complex projects, it may be better to divide the porting into two stages.
``futurize`` supports a ``--stage1`` flag for safe changes that modernize the
code but do not break Python 2.6 compatibility or introduce a depdendency on the
``future`` package. Calling ``futurize --stage2`` then completes the process.


Automatic translation
---------------------

The ``past`` package can now automatically translate some simple Python 2
modules to Python 3 upon import. The goal is to support the "long tail" of
real-world Python 2 modules (e.g. on PyPI) that have not been ported yet. For
example, here is how to use a Python 2-only package called ``plotrique`` on
Python 3. First install it:

.. code-block:: bash

    $ pip3 install plotrique==0.2.5-7 --no-compile   # to ignore SyntaxErrors
    
(or use ``pip`` if this points to your Py3 environment.)

Then pass a whitelist of module name prefixes to the ``autotranslate()`` function.
Example:

.. code-block:: bash
    
    $ python3

    >>> from past import autotranslate
    >>> autotranslate(['plotrique'])
    >>> import plotrique

This transparently translates and runs the ``plotrique`` module and any
submodules in the ``plotrique`` package that ``plotrique`` imports.

This is intended to help you migrate to Python 3 without the need for all
your code's dependencies to support Python 3 yet. It should be used as a
last resort; ideally Python 2-only dependencies should be ported
properly to a Python 2/3 compatible codebase using a tool like
``futurize`` and the changes should be pushed to the upstream project.

Note: the translation feature is still in alpha and needs more testing and
development.

Next steps
----------
Check out the `Quickstart Guide <http://python-future.org/quickstart.html>`_.


Credits and Licensing
---------------------

:Author:  Ed Schofield
:Sponsor: Python Charmers Pty Ltd, Australia, and Python Charmers Pte
          Ltd, Singapore. http://pythoncharmers.com
:Others:  See `Credits <http://python-future.org/credits.html>`_.

Copyright 2013-2014 Python Charmers Pty Ltd, Australia.

The software is distributed under an MIT licence. See LICENSE.txt or `Licensing
<http://python-future.org/licensing.html>`_.

