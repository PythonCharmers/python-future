"""
For the ``future`` package.

Turns any print statements into functions and a this import line:

    from __future__ import print_function

at the top to retain compatibility with Python 2.6+.
"""

# from lib2to3.fixer_base import BaseFix
# from lib2to3.fixer_util import FromImport, Newline, find_root
# # from lib2to3.fixer_util import Call, Name, is_probably_builtin
# from lib2to3.fixer_util import touch_import, is_import, does_tree_import
# from lib2to3.pytree import Leaf, Node
# from lib2to3.pygram import python_symbols as syms
# from lib2to3.pgen2 import token

# from future.modified_builtins import super
from lib2to3.fixes.fix_print import FixPrint
from libfuturize.fixer_util import future_import

class FixPrintWithImport(FixPrint):
    def transform(self, node, results):
        n_stmt = super(FixPrintWithImport, self).transform(node, results)
        future_import(u'print_function', node)
        return n_stmt

