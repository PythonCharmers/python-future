.. _overview:

Overview
========

``future`` is the missing compatibility layer between Python 3 and Python
2. It allows you to maintain a single, clean Python 3.x-compatible
codebase with minimal cruft and run it easily on Python 2 without further
modification.

.. _features:

**Features:**

-   backports or remappings for 15 builtins with different semantics on
	Py3 versus Py2
-   supports the reorganized Py3 standard library interface
-   220+ unit tests
-   clean on Py3: ``future`` imports and decorators have no effect on Py3
	(and no namespace pollution)
-   ``futurize`` script for automatic conversion from either Py2 or Py3
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
    
followed by standard Python 3 code. The imports allow this code to run
unchanged on Python 3 and Python 2.7.

For example, after these imports, this code runs identically on Python 3
and 2.7::
    
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


Next steps
----------
Check out the :ref:`quickstart-guide`.

