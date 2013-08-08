"""
For the ``future`` package.

Changes any imports needed to reflect the standard library reorganization. Also
Also adds this import line:

    from future import standard_library

after any __future__ imports but before any other imports.
"""

from lib2to3.fixer_util import FromImport, Newline, find_root
from lib2to3.fixer_util import touch_import, is_import, does_tree_import
from lib2to3.pytree import Leaf, Node
from lib2to3.pygram import python_symbols as syms
from lib2to3.pgen2 import token
from lib2to3.fixes.fix_imports import FixImports

from libfuturize.fixer_util import check_future_import


class FixFutureStandardLibrary(FixImports):
    def transform(self, node, results):
        result = super(FixFutureStandardLibrary, self).transform(node, results)
        # TODO: add a blank line between any __future__ imports and this?
        touch_import_top(u'future', u'standard_library', node)
        return result

