from past.builtins.noniterators import (filter, map, range, zip)
# from past.builtins.misc import (ascii, chr, hex, input, oct, open, raw_input, unichr)
from past.builtins.types import basestring, dict, str   #, unicode

from past import utils


if utils.PY3:
    # We only import names that shadow the builtins on Py3. No other namespace
    # pollution on Py3.
    
    # Only shadow builtins on Py3; no new names
    __all__ = ['filter', 'map', 'range', 'zip', 
               'basestring', 'dict', 'str',
    #            'ascii', 'chr', 'hex', 'input', 'oct', 'open', 'unichr',
    #            'bytes', 'dict', 'int', 'range', 'round', 'str', 'super',
              ]

else:
    # No namespace pollution on Py2
    __all__ = []

    # TODO: add 'callable' for Py3.0 and Py3.1?
