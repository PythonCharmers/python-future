"""
A module that brings in equivalents of the new and modified Python 3
builtins into Py2. Has no effect on Py3.

The builtin functions are:

- ``ascii``
- ``hex``
- ``oct``
- ``input`` (equivalent to ``raw_input`` on Py2)
- ``chr`` (equivalent to ``unichr`` on Py2)
- ``int`` (equivalent to ``long`` on Py2)

More will be added soon ...

"""

from . import six

if not six.PY3:
    from future_builtins import ascii, oct, hex
    from __builtin__ import unichr as chr
    # Was:
    # from __builtin__ import long as int
    # Was this safe? Probably not: it makes isinstance(1, int) == False
    # Stick to this:
    from __builtin__ import int
    __all__ = ['ascii', 'oct', 'hex', 'input', 'chr', 'int']
else:
    import builtins
    ascii, oct, hex = builtins.ascii, builtins.oct, builtins.hex
    chr = builtins.chr
    int = builtins.int
    __all__ = []
