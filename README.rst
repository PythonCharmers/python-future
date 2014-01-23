future: an easier, safer, cleaner upgrade path to Python 3
==========================================================


Overview
========


``python-future`` is the missing compatibility layer between Python 3 and
Python 2. It allows you to maintain a single, clean Python 3.x-compatible
codebase with minimal cruft and run it easily on Python 2 mostly unchanged.

It provides ``future`` and ``past`` packages with backports and forward ports
of features from Python 3 and 2. It also comes with ``futurize``, a customized
2to3-based script that helps you to transition to supporting both Python 2 and
3 in a single codebase, module by module, from either Python 2 or Python 3.


.. _features:

Features
--------

-   ``future`` package provides backports and remappings for 16 builtins with
    different semantics on Py3 versus Py2

-   ``future`` package provides backports and remappings from the Py3 standard
    library

-   330+ unit tests

-   ``futurize`` script based on ``2to3`` and parts of ``3to2`` and
    ``python-modernize``, for automatic conversion from either Py2 or Py3
    to a clean single-source codebase compatible with Python 2.6+ and
    Python 3.3+.

-   a comprehensive set of utility functions and decorators selected from
    Py2/3 compatibility interfaces from projects like ``six``, ``IPython``,
    ``Jinja2``, ``Django``, and ``Pandas``.

-   ``past`` package provides forward-ports of Python 2 types and resurrects
    some Python 2 builtins (to aid with per-module code migrations)

-   [Experimental] ``future.autoconvert`` module supports importing and
    using Python 2 modules on Python 3. This feature is still in alpha
    and needs further development to support a full range of real-world
    Python 2 modules.


Code examples
-------------

``future`` is designed to be imported at the top of each Python module
together with Python's built-in ``__future__`` module. For example, this
code behaves the same way on Python 2.6/2.7 after these imports as it does
on Python 3::
    
    from __future__ import absolute_import, division, print_function
    from future import bytes, str, open, super, zip, round, input, int

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
    assert repr(s) == 'ABCD'      # consistent repr with Py3 (no u prefix)
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
    assert isinstance('blah', str)       # if unicode_literals is in effect


There is also support for renamed standard library modules in the form of import hooks::

    from future import standard_library
    standard_library.install_hooks()

    from http.client import HttpConnection
    from itertools import filterfalse
    import html.parser
    import queue

To disable these at the end of a module, use::

    standard_library.remove_hooks()


There is also a context manager version which removes the hooks at the
end of the block::

    from future import standard_library

    with standard_library.enable_hooks():
        from http.client import HttpConnection
        from itertools import filterfalse
        import html.parser
        import queue


Documentation
-------------

See http://python-future.org


Credits
-------

:Author:  Ed Schofield
:Sponsor: Python Charmers Pty Ltd, Australia, and Python Charmers Pte
          Ltd, Singapore. http://pythoncharmers.com
:Others:  See http://python-future.org/credits.html


Licensing
---------
Copyright 2013-2014 Python Charmers Pty Ltd, Australia.
The software is distributed under an MIT licence. See LICENSE.txt.

