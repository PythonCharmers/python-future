"""
This module is designed to be used as follows::

    from future.builtins.iterators import *

And then, for example::

    for i in range(10**15):
        pass
    
    for (a, b) in zip(range(10**15), range(-10**15, 0)):
        pass

Note that this is standard Python 3 code, plus some imports that do
nothing on Python 3.

The iterators this brings in are::

- ``range``
- ``filter``
- ``map``
- ``zip``

On Python 2, ``range`` is a pure-Python backport of Python 3's ``range``
iterator with slicing support. The other iterators (``filter``, ``map``,
``zip``) are from the ``itertools`` module on Python 2. On Python 3 these
are available in the module namespace but not exported for * imports via
__all__ (zero no namespace pollution).

Note that these are also available in the standard library
``future_builtins`` module on Python 2 -- but not Python 3, so using
the standard library version is not portable, nor anywhere near complete.
"""

from __future__ import division, absolute_import, print_function

import itertools
from future import utils
from future.builtins.backports import range

if not utils.PY3:
    map = itertools.imap
    zip = itertools.izip
    filter = itertools.ifilter
    __all__ = ['range', 'map', 'zip', 'filter']
else:
    import builtins
    map = builtins.map
    zip = builtins.zip
    filter = builtins.filter
    __all__ = []

