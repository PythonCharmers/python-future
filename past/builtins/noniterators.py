"""
This module is designed to be used as follows::

    from past.builtins.noniterators import filter, map, range, reduce, zip

And then, for example::

    assert isinstance(range(5), list)
    
The list-producing functions this brings in are::

- ``filter``
- ``map``
- ``range``
- ``reduce``
- ``zip``

"""

from __future__ import division, absolute_import, print_function

import itertools
from past.utils import PY3

if PY3:
    import builtins

    # list-producing versions of the major Python iterating functions
    def oldfilter(*args, **kwargs):
        return list(builtins.filter(*args, **kwargs))

    def oldmap(*args, **kwargs):
        return list(builtins.map(*args, **kwargs))

    def oldrange(*args, **kwargs):
        return list(builtins.range(*args, **kwargs))

    # def reduce(*args, **kwargs):
    #     return list(reduce(*args, **kwargs))

    def oldzip(*args, **kwargs):
        return list(builtins.zip(*args, **kwargs))

    filter = oldfilter
    map = oldmap
    range = oldrange
    zip = oldzip
    __all__ = ['filter', 'map', 'range', 'zip']

else:
    import __builtin__
    # Python 2-builtin ranges produce lists
    filter = __builtin__.filter
    map = __builtin__.map
    # reduce = __builtin__.reduce
    range = __builtin__.range
    zip = __builtin__.zip
    __all__ = []

