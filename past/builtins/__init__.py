from past.builtins.noniterators import (filter, map, range, zip)
from past.builtins.types import basestring, dict, str   #, unicode
# from past.builtins.misc import (ascii, chr, hex, input, oct, open, raw_input, unichr)
from past.builtins.misc import cmp, execfile, raw_input, unichr, unicode

from past import utils


if utils.PY3:
    # We only import names that shadow the builtins on Py3. No other namespace
    # pollution on Py3.
    
    # Only shadow builtins on Py3; no new names
    __all__ = ['filter', 'map', 'range', 'zip', 
               'basestring', 'dict', 'str',
               'cmp', 'execfile', 'raw_input', 'unichr', 'unicode'
    #            'ascii', 'chr', 'hex', 'input', 'oct', 'open', 'unichr',
    #            'bytes', 'dict', 'int', 'range', 'round', 'str', 'super',
              ]

else:
    # No namespace pollution on Py2
    __all__ = []
