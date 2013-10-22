"""
Fixer for adding:

    from __future__ import absolute_import, division, print_function

This is "stage 1": hopefully uncontroversial changes.

Stage 2 adds ``unicode_literals``.
"""

from lib2to3 import fixer_base
# from lib2to3.pygram import python_symbols as syms
from libfuturize.fixer_util import future_import

class FixAddFutureImports(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = "file_input"

    run_order = 10

    # def match(self, node):
    #     """
    #     Match only once per file
    #     """
    #     if hasattr(node, 'type') and node.type == syms.file_input:
    #         import pdb
    #         pdb.set_trace()
    #         return True
    #     return False

    def transform(self, node, results):
        # if node.type == token.NAME:
        future_import(u"absolute_import, division, print_function", node)
        # return Name(u"str", prefix=node.prefix)

