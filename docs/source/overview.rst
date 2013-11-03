.. _overview:

Overview
========

``future`` is the missing compatibility layer between Python 3 and Python
2. It allows you to maintain a single, clean Python 3.x-compatible
codebase with minimal cruft and run it easily on Python 2 without further
modification.


.. _features:

Features
--------

-   provides backports and remappings for 15 builtins with different
    semantics on Py3 versus Py2
-   provides backports and remappings from the Py3 standard library
-   300+ unit tests
-   2to3-based ``futurize`` script for automatic conversion from either Py2 or Py3
    to a clean single-source codebase compatible with both Py3 and Py2
-   a consistent set of utility functions and decorators selected from
    Py2/3 compatibility interfaces from projects like six, IPython,
    Jinja2, Django, and Pandas.


.. _code-examples:

Code examples
-------------

``future`` is designed to be imported at the top of each Python module
together with Python's built-in ``__future__`` module like this::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future import standard_library
    from future.builtins import *
    
followed by standard Python 3 code. The imports have no effect on Python
3 but allow the code to run mostly unchanged on Python 3 and Python 2.6/2.7.

For example, after these imports, this code runs identically on Python 3
and 2.6/2.7::
    
    # Support for renamed standard library modules via import hooks
    from http.client import HttpConnection
    from itertools import filterfalse
    import html.parser
    import queue

    # Backported Py3 bytes object
    b = bytes(b'ABCD')
    assert list(b) == [65, 66, 67, 68]
    assert repr(b) == "b'ABCD'"
    # These raise TypeErrors:
    # b + u'EFGH'
    # bytes(b',').join([u'Fred', u'Bill'])

    # Backported Py3 str object
    s = str(u'ABCD')
    assert s != b'ABCD'
    assert isinstance(s.encode('utf-8'), bytes)
    assert isinstance(b.decode('utf-8'), str)
    assert repr(s) == 'ABCD'      # consistent repr with Py3 (no u prefix)
    # These raise TypeErrors:
    # b'B' in s
    # s.find(b'A')

    # Extra arguments for the open() function
    f = open('japanese.txt', encoding='utf-8', errors='replace')
    
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
    
    # The round() function behaves as it does in Python 3, using
    # "Banker's Rounding" to the nearest even last digit:
    assert round(0.1250, 2) == 0.12
    
    # input() replaces Py2's raw_input() (with no eval()):
    name = input('What is your name? ')
    print('Hello ' + name)

    # Compatible output from isinstance() across Py2/3:
    assert isinstance(2**63, int)        # long integers
    assert isinstance(u'blah', str)
    assert isinstance('blah', str)       # with unicode_literals in effect


Next steps
----------
Check out the :ref:`quickstart-guide`.

