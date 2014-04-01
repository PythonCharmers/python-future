"""
For the ``future`` package.

Changes any imports needed to reflect the standard library reorganization. Also
Also adds this import line:

    from future import standard_library

after any __future__ imports but before any other imports.
"""
from __future__ import absolute_import, unicode_literals

from lib2to3.fixes.fix_imports import FixImports, MAPPING
from libfuturize.fixer_util import touch_import_top
# Local imports
from lib2to3.pgen2 import token
from lib2to3.pytree import Leaf, Node
from lib2to3.pygram import python_symbols as syms
from lib2to3 import patcomp

from future.builtins import str


mapping = {}


# These modules exist on Py2 and Py2.7 so they needn't be replaced by
# future.standard_library.io etc.:
IN_PY2 = ['io', 'pickle', 'collections', 'subprocess']

for (old, new) in MAPPING.items():
    if new in IN_PY2:
        continue
    # Change e.g. urllib.request to urllib_request
    # if '.' in new:
    #     new.replace('.', '_')
    mapping[old] = ('future.standard_library.' + new,
                    new.replace('.', '_'))


class FixFutureStandardLibrary(FixImports):
    run_order = 8
    mapping = mapping

    def transform(self, node, results):
        import_mod = results.get("module_name")
        import pdb
        pdb.set_trace()

        if import_mod:
            mod_name = import_mod.value
            new_name1, new_name2 = map(str, self.mapping[mod_name])
            # import_mod.replace(Name(new_name, prefix=import_mod.prefix))
            children = [Leaf(token.NAME, new_name1, prefix=u" "),
                        Leaf(token.NAME, u"as", prefix=u" "),
                        Leaf(token.NAME, new_name2, prefix=u" ")]
            # newnode = Node(syms.dotted_as_name, children)]
            imp = Node(syms.dotted_as_name, children)
            import_mod.replace(imp) # Node(dotted_as_name,
                                    # [Name(new_name, prefix=import_mod.prefix),
                                    #  Node(dotted_as_name,
                                    #       [Leaf(1, u'ConfigParser'),
                                    #        Leaf(1, u'as'),
                                    #        Leaf(1, new_name.replace('.', '_'))
                                    #       ])
                                    # ]))
            if "name_import" in results:
                # If it's not a "from x import x, y" or "import x as y" import,
                # marked its usage to be replaced.
                self.replace[mod_name] = new_name2
            if "multiple_imports" in results:
                # This is a nasty hack to fix multiple imports on a line (e.g.,
                # "import StringIO, urlparse"). The problem is that I can't
                # figure out an easy way to make a pattern recognize the keys of
                # MAPPING randomly sprinkled in an import statement.
                results = self.match(node)
                if results:
                    self.transform(node, results)
        else:
            # Replace usage of the module.
            bare_name = results["bare_with_attr"][0]
            new_name = self.replace.get(bare_name.value)
            if new_name:
                bare_name.replace(Name(new_name, prefix=bare_name.prefix))

    # def transform(self, node, results):
    #     import pdb
    #     pdb.set_trace()
    #     result = super(FixFutureStandardLibrary, self).transform(node, results)
    #     # TODO: add a blank line between any __future__ imports and this?
    #     touch_import_top(u'future', u'standard_library', node)
    #     return result


