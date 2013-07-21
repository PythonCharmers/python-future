"""
This module is designed to be used as follows:

    from __future__ import division, absolute_import, print_function
    from future import common_iterators

And then, for example:

    for i in range(10**10):
        pass

    for (a, b) in zip(range(10**10), range(-10**10, 0, -1)):
        pass

Note that this is standard Python 3 code, plus some imports that do
nothing on Python 3.

The iterators this brings in are:
- range
- filter
- map
- zip

range is equivalent to xrange on Python 2 by default. As an alternative,
there is a pure Python backport of Python 3's range iterator available
with slicing support. To use it, add:

    from future.features import range

The other iterators (filter, map, zip) are from the itertools module on
Python 2.
"""

from __future__ import division, absolute_import, print_function

import inspect
from . import six

_oldrange, _oldmap, _oldzip, _oldfilter = range, map, zip, filter

from .six.moves import xrange as range
from .six.moves import map, zip, filter


if not six.PY3:
    caller = inspect.currentframe().f_back
    caller.f_globals.update(range=range, map=map, zip=zip, filter=filter)
    caller.f_globals.update(_oldrange=_oldrange, _oldmap=_oldmap,
                            _oldzip=_oldzip, _oldfilter=_oldfilter)

