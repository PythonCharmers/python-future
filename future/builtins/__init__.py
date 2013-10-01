"""
A module that brings in equivalents of the new and modified Python 3
builtins into Py2. Has no effect on Py3.

See the docs for these modules for more information::

- future.builtins.iterators
- future.builtins.backports
- future.builtins.str_as_unicode
- future.builtins.misc
- future.builtins.disabled

"""

from future.builtins.iterators import (filter, map, zip)
from future.builtins.misc import (ascii, oct, hex, chr, int, input, open)
from future.builtins.backports import (str, bytes, range, round, super)
from future import utils

if not utils.PY3:
    # We only import names that shadow the builtins on Py2. No other namespace
    # pollution on Py2.
    from future.builtins.disabled import (apply, cmp, coerce,
            execfile, file, long, raw_input, reduce, reload, unicode,
            xrange, StandardError)
    
    # Only shadow builtins on Py2; no new names
    __all__ = ['filter', 'map', 'zip', 
               'ascii', 'oct', 'hex', 'chr', 'int', 'input', 'open',
               'str', 'bytes', 'range', 'round', 'super',
               'apply', 'cmp', 'coerce', 'execfile', 'file', 'long',
               'raw_input', 'reduce', 'reload', 'unicode', 'xrange',
               'StandardError']

else:
    # No namespace pollution on Py3
    __all__ = []

    # TODO: add 'callable' for Py3.0 and Py3.1?
