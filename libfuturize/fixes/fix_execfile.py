# coding: utf-8
"""
Fixer for the execfile() function on Py2, which was removed in Py3.

The Lib/lib2to3/fixes/fix_execfile.py module has some problems: see
python-future issue #37. This fixer merely imports execfile() from
past.builtins and leaves the code alone.

Adds this import line::

    from past.builtins import cmp
    from past.builtins import execfile

for each of the functions cmp, execfile that were removed from Py3.

Adds these imports after any other imports (in an initial block of them).
"""

from __future__ import unicode_literals

from lib2to3 import fixer_base
from lib2to3.pygram import python_symbols as syms
from lib2to3.fixer_util import Name, Call, in_special_context

from libfuturize.fixer_util import touch_import_top


replaced_builtins = '''cmp execfile'''.split()

expression = '|'.join(["name='{0}'".format(name) for name in replaced_builtins])


class FixExecfile(fixer_base.BaseFix):
    BM_compatible = True
    run_order = 9

    PATTERN = """
              power<
                 ({0}) trailer< '(' args=[any] ')' >
              rest=any* >
              """.format(expression)

    def transform(self, node, results):
        name = results["name"]
        touch_import_top(u'past.builtins', name.value, node)

