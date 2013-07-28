"""
For the ``future`` package.

Use:
  $ python modernize.py --print-function --future-unicode --no-six \
                        --fix=libmodernize.fixes.fix_future_package testme.py

Adds these import lines:

    import future.standard_library_renames
    from future import *

to invoke the 3rd-party ``future`` package to provide Py2 compatibility for the output of 2to3.
"""

from lib2to3.fixer_base import BaseFix
from lib2to3.fixer_util import FromImport, Newline, find_root
# from lib2to3.fixer_util import Call, Name, is_probably_builtin
from lib2to3.fixer_util import touch_import, is_import, does_tree_import
from lib2to3.pytree import Leaf, Node
from lib2to3.pygram import python_symbols as syms
from lib2to3.pgen2 import token
# from lib2to3.patcomp import PatternCompiler
from libmodernize import check_future_import
# from libmodernize import add_future


def add_future(node, symbol):
    root = find_root(node)

    for idx, node in enumerate(root.children):
        if node.type == syms.simple_stmt and \
           len(node.children) > 0 and node.children[0].type == token.STRING:
            # skip over docstring
            continue
        names = check_future_import(node)
        if not names:
            # not a future statement; need to insert before this
            break
        if symbol in names:
            # already imported
            return

    import_ = FromImport('__future__', [Leaf(token.NAME, symbol, prefix=" ")])
    children = [import_, Newline()]
    root.insert_child(idx, Node(syms.simple_stmt, children))


# class FixAllFutureImports(BaseFix):
#     def match(self, node):
#         if node.type == syms.file_input:
#             return True
#         return False
# 
#     def transform(self, node, results):
#         import pdb
#         pdb.set_trace()
#         add_future(node, u'absolute_import')
#         add_future(node, u'division')
#         add_future(node, u'print_function')
#         add_future(node, u'unicode_literals')

        
class FixFuturePackage(BaseFix):

    def match(self, node):
        if node.type == syms.file_input:
            return True
        return False
        # if is_import(node):
        #     return True
        # return False
    
    def transform(self, node, results):
        touch_import_top(u'__future__', u'absolute_import', node)
        touch_import_top(u'__future__', u'division', node)
        touch_import_top(u'__future__', u'print_function', node)
        touch_import_top(u'__future__', u'unicode_literals', node)
        # add_future(node, u'unicode_literals')
        touch_import_top(None, u'future.standard_library', node)
        touch_import(u'future', u'*', node)
       
def is_import_from(node):
    """Returns true if the node is a statement "from ... import ..."
    """
    return node.type == syms.import_from


def touch_import_top(package, name, node):
    """ Works like `does_tree_import` but adds an import statement at the top
        if it was not imported (but after any __future__ imports).
        
        Based on lib2to3.fixer_util.touch_import() """

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

    root = find_root(node)

    if does_tree_import(package, name, root):
        return

    # try to find the first import, and insert above that, unless it's a
    # __future__ import
    insert_pos = offset = 0
    for idx, node in enumerate(root.children):
        if not is_import_stmt(node):
            continue
        else:
            if is_future_import_stmt(node):
                continue
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


def add_future_package_import(node, symbol):
    import pdb
    pdb.set_trace()
    root = find_root(node)
    for idx, node in enumerate(root.children):
        if node.type == syms.simple_stmt and \
           len(node.children) > 0 and node.children[0].type == token.STRING:
            # skip over docstring
            continue
        names = check_future_import(node)
        if not names:
            # not a future statement; need to insert before this
            break
        if symbol in names:
            # already imported
            return

    import_ = FromImport('future', [Leaf(token.NAME, symbol, prefix=" ")])
    children = [import_, Newline()]
    root.insert_child(idx, Node(syms.simple_stmt, children))

# ###
# # Examples from http://python3porting.com/fixers.html:
# class FixName1(BaseFix):
#     
#     _accept_type = token.NAME
# 
#     def match(self, node):
#         if node.value == 'oldname':
#             return True
#         return False
#     
#     def transform(self, node, results):
#         node.value = 'newname'
#         node.changed()
# 
# class FixConstant(BaseFix):
#         
#     PATTERN = """
#         import_name< 'import' modulename='foo' >
#         |
#         import_name< 'import' dotted_as_name< 'foo' 'as'
#            modulename=any > >
#         |
#         import_from< 'from' 'foo' 'import'
#            importname='CONSTANT' >
#         |
#         import_from< 'from' 'foo' 'import' import_as_name<
#            importname='CONSTANT' 'as' constantname=any > >
#         |
#         any
#         """
# 
#     def start_tree(self, tree, filename):
#         super(FixConstant, self).start_tree(tree, filename)
#         # Reset the patterns attribute for every file:
#         self.usage_patterns = []
#         
#     def match(self, node):
#         # Match the import patterns:
#         results = {"node": node}
#         match = self.pattern.match(node, results)
#         
#         if match and 'constantname' in results:
#             # This is an "from import as"
#             constantname = results['constantname'].value
#             # Add a pattern to fix the usage of the constant
#             # under this name:
#             self.usage_patterns.append(
#                 PatternCompiler().compile_pattern(
#                     "constant='%s'"%constantname))
#             return results
#         
#         if match and 'importname' in results:
#             # This is a "from import" without "as".
#             # Add a pattern to fix the usage of the constant
#             # under it's standard name:
#             self.usage_patterns.append(
#                 PatternCompiler().compile_pattern(
#                     "constant='CONSTANT'"))
#             return results
#         
#         if match and 'modulename' in results:
#             # This is a "import as"
#             modulename = results['modulename'].value
#             # Add a pattern to fix the usage as an attribute:
#             self.usage_patterns.append(
#                 PatternCompiler().compile_pattern(
#                 "power< '%s' trailer< '.' " \
#                 "attribute='CONSTANT' > >" % modulename))
#             return results
#         
#         # Now do the usage patterns
#         for pattern in self.usage_patterns:
#             if pattern.match(node, results):
#                 return results
#     
#     def transform(self, node, results):
#         if 'importname' in results:
#             # Change the import from CONSTANT to get_constant:
#             node = results['importname']
#             node.value = 'get_constant'
#             node.changed()
#             
#         if 'constant' in results or 'attribute' in results:
#             if 'attribute' in results:
#                 # Here it's used as an attribute.
#                 node = results['attribute']
#             else:
#                 # Here it's used standalone.
#                 node = results['constant']
#                 # Assert that it really is standalone and not
#                 # an attribute of something else, or an
#                 # assignment etc:
#                 if not is_probably_builtin(node):
#                     return None
#                 
#             # Now we replace the earlier constant name with the
#             # new function call. If it was renamed on import
#             # from 'CONSTANT' we keep the renaming else we
#             # replace it with the new 'get_constant' name:
#             name = node.value
#             if name == 'CONSTANT':
#                 name = 'get_constant'
#             node.replace(Call(Name(name), prefix=node.prefix))
