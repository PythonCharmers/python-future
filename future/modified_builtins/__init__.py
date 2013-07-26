"""
This module contains backports of new or changed functionality from
Python 3 to Python 2.

For example:
- a Python 2 backport of the range iterator from Py3 with slicing
  support.
- the magic zero-argument super() function
- the new round() behaviour

It is used as follows:

    from __future__ import division, absolute_import, print_function
    from future.modified_builtins import (range, super, round, input)

to bring in the new semantics for these functions from Python 3. And
then, for example:

    for i in range(10**11)[:10]:
        pass

and:

    class VerboseList(list):
        def append(self, item):
            print('Adding an item')
            super().append(item)    	# new simpler super() function

Notes
=====

range()
-------
range is a custom class that backports the slicing behaviour from
Python 3 (from the xrange module by Dan Crosta). See the
docstring for more details.


super()
-------
super() is based on Ryan Kelly's magicsuper module. See the docstring for
more details.


input()
-------
Like the new safe input() function from Python 3 (without eval()), except
that it returns bytes. Equivalent to Python 2's raw_input().

By default, the old Python 2 input() is **removed** from __builtin__ for
safety (because it may otherwise lead to shell injection on Python 2 if
used accidentally after forgetting to import the replacement for some
reason.

To restore it, you can retrieve it yourself from __builtin__._old_input.

round()
-------
Python 3 modifies the behaviour of round() to use "Banker's Rounding".
See http://stackoverflow.com/a/10825998. See the docstring for more
details.


TODO:
-----
- Check int() ??

"""

from __future__ import division, absolute_import, print_function

from future import six

if six.PY3:
    import builtins
    range = builtins.range
    super = builtins.super
    round = builtins.round
    input = builtins.input
    __all__ = []
else:
    from .newsuper import super
    from .newrange import range
    from .newround import round

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

    __all__ = ['range', 'super', 'round', 'input']
