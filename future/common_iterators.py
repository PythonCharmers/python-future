"""
This module is designed to be used as follows:

    from __future__ import division, absolute_import, print_function
    from future import common_iterators

And then, for example:

    for i in range(10**8):
        pass

Note that this is standard Python 3 code, plus some imports that do nothing
on Python 3.

The iterators this brings in are:
- range
- filter
- map
- zip
"""

from __future__ import division, absolute_import, print_function

import inspect
import six

from six.moves import xrange as range
from six.moves import map, zip, filter

caller = inspect.currentframe().f_back
caller.f_globals.update(range=range, map=map, zip=zip, filter=filter)
