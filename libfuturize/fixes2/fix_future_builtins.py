"""
For the ``future`` package.

Adds this import line:

    from future import *

after any other imports.
"""

from lib2to3.fixer_base import BaseFix
# from lib2to3.fixer_util import FromImport, Newline, find_root
from lib2to3.fixer_util import touch_import # , is_import, does_tree_import
# from lib2to3.pytree import Leaf, Node
from lib2to3.pygram import python_symbols as syms
# from lib2to3.pgen2 import token

       
class FixFutureBuiltins(BaseFix):

    def match(self, node):
        if node.type == syms.file_input:
            return True
        return False
        # if is_import(node):
        #     return True
        # return False
    
    def transform(self, node, results):
        touch_import(u'future', u'*', node)

