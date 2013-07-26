"""
This module is designed to be used as follows::

    from __future__ import division, absolute_import, print_function
    from future.modified_builtins import (input, round, super, range)

To bring in the new semantics for these functions from Python 3.

Notes
=====

input()
-------
The old Python 2 input() is **removed** from __builtin__ for safety (because it
may otherwise lead to shell injection on Python 2 if used accidentally after
forgetting to import the replacement for some reason.


round()
-------
Python 3 modifies the behaviour of round() to use "Banker's Rounding".

See http://stackoverflow.com/a/10825998.


TODO:
-----
- Check int() ??

"""

from __future__ import division, absolute_import, print_function

from . import six

if not six.PY3:

    from future.features.newsuper import super
    from future.features.newrange import range
    from future.features.newround import round

    # Python 2's input() is unsafe and MUST not be able to be used
    # accidentally by someone who forgets to import it but expects Python
    # 3 semantics. So we delete it from __builtin__. We keep a copy
    # though:
    import __builtin__
    __builtin__._oldinput = __builtin__.input
    delattr(__builtin__, 'input')

    # New one with Py3 semantics:
    __builtin__.input = six.moves.input
    input = six.moves.input
    input.__doc__ = """
input([prompt]) -> string

Like the new safe input() function from Python 3 (without eval()), except that
it returns bytes. Equivalent to Python 2's raw_input().

For example, the following code (from the 2to3 Porting Guide) works on both Python 3 and 2:

    def greet(name):
        print("Hello, {0}!".format(name))

    print("What's your name?")
    name = input()
    greet(name)
"""


