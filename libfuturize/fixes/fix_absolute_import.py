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
from lib2to3.fixer_util import FromImport, syms
from lib2to3.fixes.fix_import import traverse_imports
from libfuturize.fixer_util import future_import

class FixAbsoluteImport(FixImport):
    run_order = 9

    def transform(self, node, results):
        """
        Copied from FixImport.transform(), but with this line added in
        any modules that had implicit relative imports changed:

            from __future__ import absolute_import"
        """
        if self.skip:
            return
        imp = results['imp']

        if node.type == syms.import_from:
            # Some imps are top-level (eg: 'import ham')
            # some are first level (eg: 'import ham.eggs')
            # some are third level (eg: 'import ham.eggs as spam')
            # Hence, the loop
            while not hasattr(imp, 'value'):
                imp = imp.children[0]
            if self.probably_a_local_import(imp.value):
                imp.value = u"." + imp.value
                imp.changed()
                future_import(u"absolute_import", node)
        else:
            have_local = False
            have_absolute = False
            for mod_name in traverse_imports(imp):
                if self.probably_a_local_import(mod_name):
                    have_local = True
                else:
                    have_absolute = True
            if have_absolute:
                if have_local:
                    # We won't handle both sibling and absolute imports in the
                    # same statement at the moment.
                    self.warning(node, "absolute and local imports together")
                return

            new = FromImport(u".", [imp])
            new.prefix = node.prefix
            future_import(u"absolute_import", node)
            return new

    # This always adds "from __future__ import absolute_import":
    # def transform(self, node, results):
    #     result = super(FixAbsoluteImport, self).transform(node, results)
    #     future_import(u"absolute_import", node)
    #     return result

