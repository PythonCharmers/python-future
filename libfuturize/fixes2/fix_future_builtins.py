"""
For the ``future`` package.

Adds this import line::

    from future.builtins import XYZ

for each of the functions XYZ that is used in the module from those in
future.builtins.

Adds these imports after any other imports (in an initial block of them).
"""

from __future__ import unicode_literals

from lib2to3 import fixer_base
from lib2to3.pygram import python_symbols as syms
from libfuturize.fixer_util import touch_import_top

       
"""
Fixer that changes zip(seq0, seq1, ...) into list(zip(seq0, seq1, ...)
unless there exists a 'from future_builtins import zip' statement in the
top-level namespace.

We avoid the transformation if the zip() call is directly contained in
iter(<>), list(<>), tuple(<>), sorted(<>), ...join(<>), or for V in <>:.
"""

# Local imports
from lib2to3.fixer_util import Name, Call, in_special_context

# from future.builtins.iterators import (filter, map, zip)
# from future.builtins.misc import (ascii, chr, hex, input, isinstance, oct, open)
# from future.builtins.backports import (bytes, int, range, round, str, super)

replaced_builtins = '''filter map zip
                       ascii chr hex input isinstance oct open bytes int range
                       bytes int range round str super'''.split()

expression = '|'.join(["name='{}'".format(name) for name in replaced_builtins])


class FixFutureBuiltins(fixer_base.BaseFix):
    BM_compatible = True
    run_order = 8

    # Example:
    # PATTERN = """
    #           power<
    #              (name='print'|name='input'|name='raw_input') trailer< '(' args=[any] ')' >
    #           rest=any* >
    #           """

    PATTERN = """
              power<
                 ({}) trailer< '(' args=[any] ')' >
              rest=any* >
              """.format(expression)

    def transform(self, node, results):
        name = results["name"]
        touch_import_top(u'future.builtins', name.value, node)
        # name.replace(Name(u"input", prefix=name.prefix))



