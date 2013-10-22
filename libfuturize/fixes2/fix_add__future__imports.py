"""
Fixer for adding:

    from __future__ import absolute_import, division, print_function

This is "stage 1": hopefully uncontroversial changes.

Stage 2 adds ``unicode_literals``.
"""

from libfuturize.fixer_util import future_import

class FixAddFutureImports(fixer_base.BaseFix):
    def transform(self, node, results):
        future_import(u"absolute_import, division, print_function", node)

