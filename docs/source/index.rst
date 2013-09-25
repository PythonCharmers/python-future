future: clean single-source support for Python 3 and 2
======================================================

``future`` is the missing compatibility layer between Python 3 and
Python 2. It allows you to maintain a single, clean Python
3.x-compatible codebase with minimal cruft and also run it on Python 2
without further modification.

It is designed to be used together with Python's built-in ``__future__``
imports like this::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future import standard_library
    from future.builtins import *
    
followed by standard Python 3 code, which then runs unchanged on both
Python 3 and Python 2.7. For examples, see the :ref:`overview`.


.. include:: contents.rst.inc

