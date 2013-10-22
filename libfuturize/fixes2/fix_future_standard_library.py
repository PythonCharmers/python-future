"""
For the ``future`` package.

Changes any imports needed to reflect the standard library reorganization. Also
Also adds this import line:

    from future import standard_library

after any __future__ imports but before any other imports.
"""

# from lib2to3.fixes.fix_imports import FixImports
from lib2to3 import fixer_base
from libfuturize.fixer_util import touch_import_top

# from future.standard_library import ... as modules
# standard_library_modules = 
# _pats = ["power< 'types' trailer< '.' name='%s' > >" % m for m in modules]

# class FixFutureStandardLibrary(FixImports):
class FixFutureStandardLibrary(fixer_base.BaseFix):
    BM_compatible = True
    # We don't add the import conditionally right now ...
    # PATTERN = '|'.join(_pats)
    run_order = 9
    PATTERN = "file_input"

    def transform(self, node, results):
        # TODO: add a blank line between any __future__ imports and this?
        touch_import_top(u'future', u'standard_library', node)

    # def transform(self, node, results):
    #     result = super(FixFutureStandardLibrary, self).transform(node, results)
    #     touch_import_top(u'future', u'standard_library', node)
    #     return result

