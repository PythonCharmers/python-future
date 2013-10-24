"""
Adds this import:
    
    from __future__ import unicode_literals


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

from lib2to3 import fixer_base
from libfuturize.fixer_util import future_import

class FixUnicodeLiteralsImport(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = "file_input"

    run_order = 9

    def transform(self, node, results):
        future_import(u"unicode_literals", node)

