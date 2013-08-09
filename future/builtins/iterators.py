"""
This module is designed to be used as follows::

    from __future__ import division, absolute_import, print_function
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

``range`` is equivalent to ``xrange`` on Python 2 when imported from this
module. As an alternative, there is a pure Python backport of Python 3's
``range`` iterator available with slicing support. To use it, import it with::

    from future.builtins.backports import range

The other iterators (``filter``, ``map``, ``zip``) are from the ``itertools``
module on Python 2.

Note that these are also available in the standard library
``future_builtins`` module on Python 2 -- but not Python 3, so using
the standard library version is not portable, nor anywhere near complete.
"""

from __future__ import division, absolute_import, print_function

from future import six

if not six.PY3:
    _oldrange, _oldmap, _oldzip, _oldfilter = range, map, zip, filter

from future.six.moves import xrange as range
from future.six.moves import map, zip, filter

if six.PY3:
    __all__ = []
    

