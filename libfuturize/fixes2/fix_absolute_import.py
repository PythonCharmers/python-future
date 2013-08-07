"""
Fixer for import statements, with a __future__ import line.

Based on lib2to3/fixes/fix_import.py

If spam is being imported from the local directory, this import:
    from spam import eggs
becomes:
    from .spam import eggs

and this import:
    import spam
becomes:
    from . import spam
"""

from lib2to3.fixes.fix_import import FixImport
from libfuturize.fixer_util import future_import

class FixAbsoluteImport(FixImport):
    def transform(self, node, results):
        result = super(FixAbsoluteImport, self).transform(node, results)
        future_import(u"absolute_import", node)
        return result

