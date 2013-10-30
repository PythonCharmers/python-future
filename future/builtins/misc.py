"""
A module that brings in equivalents of the new and modified Python 3
builtins into Py2. Has no effect on Py3.

The builtin functions are:

- ``ascii`` (from Py2's future_builtins module)
- ``hex`` (from Py2's future_builtins module)
- ``oct`` (from Py2's future_builtins module)
- ``chr`` (equivalent to ``unichr`` on Py2)
- ``input`` (equivalent to ``raw_input`` on Py2)
- ``open`` (equivalent to io.open on Py2)

This function is also defined specially:

- ``isinstance``

to be compatible with the backported ``int``, ``str``, and ``bytes`` types of
``future.builtins``.


input()
-------
Like the new ``input()`` function from Python 3 (without eval()), except
that it returns bytes. Equivalent to Python 2's ``raw_input()``.

Warning: By default, importing this module *removes* the old Python 2
input() function entirely from ``__builtin__`` for safety. This is
because forgetting to import the new ``input`` from ``future`` might
otherwise lead to a security vulnerability (shell injection) on Python 2.

To restore it, you can retrieve it yourself from
``__builtin__._old_input``.

Fortunately, ``input()`` seems to be seldom used in the wild in Python
2...

"""

from future.builtins.backports.newint import newint
from future import utils


if utils.PY2:
    from io import open
    from future_builtins import ascii, oct, hex
    from __builtin__ import unichr as chr
    import __builtin__

    # Is it a good idea to define this? It'll mean many fewer lines of
    # type-checking code need to be changed to using custom 
    # functions (like future.utils.isint). Example: the xlwt package uses
    # isinstance() a lot. On the other hand, it may break some things and make
    # them harder to debug.
    def isinstance(obj, class_or_type_or_tuple):
        """
        isinstance(object, class-or-type-or-tuple) -> bool
        
        Return whether an object is an instance of a class or of a
        subclass thereof.  With a type as second argument, return whether
        that is the object's type.  The form using a tuple, isinstance(x,
        (A, B, ...)), is a shortcut for isinstance(x, A) or isinstance(x,
        B) or ... (etc.).
        """
        if hasattr(class_or_type_or_tuple, '__native__'):
            # Special case for Py2 short int
            if class_or_type_or_tuple == newint and isinstance(obj, int):
                return True
            return __builtin__.isinstance(obj, class_or_type_or_tuple.__base__)
        else:
            return __builtin__.isinstance(obj, class_or_type_or_tuple)

    # The following seems like a good idea, but it may be a bit
    # paranoid and the implementation may be fragile:

    # Python 2's input() is unsafe and MUST not be able to be used
    # accidentally by someone who expects Python 3 semantics but forgets
    # to import it on Python 2. So we delete it from __builtin__. We
    # keep a copy though:
    __builtin__._oldinput = __builtin__.input
    delattr(__builtin__, 'input')

    input = raw_input

    # In case some code wants to import 'callable' portably from Py3.0/3.1:
    callable = __builtin__.callable

    __all__ = ['ascii', 'chr', 'hex', 'input', 'isinstance', 'oct', 'open']

else:
    import builtins
    ascii = builtins.ascii
    chr = builtins.chr
    hex = builtins.hex
    input = builtins.input
    isinstance = builtins.isinstance
    oct = builtins.oct
    open = builtins.open

    __all__ = []

    # From Pandas, for Python versions 3.0 and 3.1 only. The callable()
    # function was removed from Py3.0 and 3.1 and reintroduced into Py3.2.
    try:
        # callable reintroduced in later versions of Python
        callable = builtins.callable
    except AttributeError:
        def callable(obj):
            return any("__call__" in klass.__dict__ for klass in type(obj).__mro__)
        __all__.append('callable')
