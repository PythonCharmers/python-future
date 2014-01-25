"""
For the ``future`` package.

Adds this import line:

    from future.builtins import *

after any other imports (in an initial block of them).
"""

from ..fixes2.fix_future_builtins import FixFutureBuiltins
