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
from future.builtins.backports import (round, range, super)
from future.builtins.str_is_unicode import str  
from future import utils

# We don't import the python_2_unicode_compatible decorator; only names
# that shadow the builtins on Py2.

if not utils.PY3:
    from future.builtins.disabled import (apply, cmp, coerce,
            execfile, file, long, raw_input, reduce, reload, unicode,
            xrange, StandardError)
    
    # Only shadow builtins on Py2; no new names
    __all__ = ['filter', 'map', 'zip', 
               'ascii', 'oct', 'hex', 'chr', 'int', 'input', 'open',
               'round', 'range', 'super',
               'apply', 'cmp', 'coerce', 'execfile', 'file', 'long',
               'raw_input', 'reduce', 'reload', 'unicode', 'xrange',
               'str',
               'StandardError']

else:
    # No namespace pollution on Py3
    __all__ = []

