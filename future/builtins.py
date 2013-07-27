"""
A module that brings in (backports of) the new and modified Python 3
builtins into Py2. Has no effect on Py3.

The builtin functions are:

- ascii
- hex
- oct
- input (equivalent to raw_input on Py2)

More will be added soon ...

"""

from . import six

if not six.PY3:
    from future_builtins import ascii, oct, hex
    from __builtin__ import unichr as chr
    from __builtin__ import long as int   # is this safe?!
    __all__ = ['ascii', 'oct', 'hex', 'input', 'chr', 'int']
else:
    import builtins
    ascii, oct, hex = builtins.ascii, builtins.oct, builtins.hex
    chr = builtins.chr
    int = builtins.int
    __all__ = []
