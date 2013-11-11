"""
A module that brings in equivalents of the new and modified Python 3
builtins into Py2. Has no effect on Py3.

See the docs for these modules for more information::

- future.builtins.iterators
- future.builtins.backports
- future.builtins.misc
- future.builtins.disabled

"""

from future.builtins.iterators import (filter, map, zip)
# The isinstance import is unneeded. For backward-compatibility with
# future v0.8 only.
from future.builtins.misc import (ascii, chr, hex, input, isinstance, oct, open)
from future.builtins.backports import (bytes, int, range, round, str, super)
from future import utils

if not utils.PY3:
    # We only import names that shadow the builtins on Py2. No other namespace
    # pollution on Py2.
    
    # Only shadow builtins on Py2; no new names
    __all__ = ['filter', 'map', 'zip', 
               'ascii', 'chr', 'hex', 'input', 'isinstance', 'oct', 'open',
               'bytes', 'int', 'range', 'round', 'str', 'super',
              ]

else:
    # No namespace pollution on Py3
    __all__ = []

    # TODO: add 'callable' for Py3.0 and Py3.1?
