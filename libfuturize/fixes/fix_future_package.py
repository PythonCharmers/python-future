"""
For the ``future`` package.

Use like this to port Python 2 code:

  $ python modernize.py --print-function --future-unicode --no-six \
                        --fix=libmodernize.fixes.fix_future_package \
                        mypython2script.py

Or, to make existing Python 3 code compatible with Python 2 using the
``future`` package:

  $ 2to3 --fix future_package --verbose mypython3script.py

Adds these import lines:

    from __future__ import absolute_import
    from __future__ import division
    from __future__ import print_function
    from __future__ import unicode_literals
    import future.standard_library_renames
    from future import *
    # other imports here

to invoke the 3rd-party ``future`` package to provide Py2 compatibility for the output of 2to3.
"""

from lib2to3.fixer_base import BaseFix
from lib2to3.fixer_util import FromImport, Newline, find_root
# from lib2to3.fixer_util import Call, Name, is_probably_builtin
from lib2to3.fixer_util import touch_import, is_import, does_tree_import
from lib2to3.pytree import Leaf, Node
from lib2to3.pygram import python_symbols as syms
from lib2to3.pgen2 import token

       
class FixFuturePackage(BaseFix):

    def match(self, node):
        if node.type == syms.file_input:
            return True
        return False
        # if is_import(node):
        #     return True
        # return False
    
    def transform(self, node, results):
        touch_import_top(u'future', u'*', node)
        touch_import_top(None, u'future.standard_library', node)
        touch_import_top(u'__future__', u'unicode_literals', node)
        touch_import_top(u'__future__', u'print_function', node)
        touch_import_top(u'__future__', u'division', node)
        touch_import_top(u'__future__', u'absolute_import', node)
        # add_future(node, u'unicode_literals')
       
def is_import_from(node):
    """Returns true if the node is a statement "from ... import ..."
    """
    return node.type == syms.import_from


def is_import_stmt(node):
    return (node.type == syms.simple_stmt and node.children and
            is_import(node.children[0]))

def is_future_import_stmt(node):
    if node.type == syms.simple_stmt and node.children:
        child = node.children[0]
        if (is_import(child) and
            is_import_from(child) and
            child.children[1].value == u'__future__'):
            return True
    return False


def touch_import_top(package, name, node):
    """Works like `does_tree_import` but adds an import statement at the
    top if it was not imported.

    Calling this multiple times adds them in reverse order.
        
    Based on lib2to3.fixer_util.touch_import()
    """

    root = find_root(node)

    if does_tree_import(package, name, root):
        return

    # try to find the first import, and insert above that
    insert_pos = offset = 0
    for idx, node in enumerate(root.children):
        if not is_import_stmt(node):
            continue
        # elif is_future_import_stmt(node):
        #     continue
        insert_pos = idx + offset
        break

    # if there are no imports where we can insert, find the docstring.
    # if that also fails, we stick to the beginning of the file
    if insert_pos == 0:
        for idx, node in enumerate(root.children):
            if (node.type == syms.simple_stmt and node.children and
               node.children[0].type == token.STRING):
                insert_pos = idx + 1
                break

    if package is None:
        import_ = Node(syms.import_name, [
            Leaf(token.NAME, u"import"),
            Leaf(token.NAME, name, prefix=u" ")
        ])
    else:
        import_ = FromImport(package, [Leaf(token.NAME, name, prefix=u" ")])

    children = [import_, Newline()]
    root.insert_child(insert_pos, Node(syms.simple_stmt, children))

