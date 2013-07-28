"""
From python-modernize by Armin Ronacher
"""
from lib2to3.fixer_util import FromImport, Newline, find_root
from lib2to3.pytree import Leaf, Node
from lib2to3.pygram import python_symbols as syms, python_grammar
from lib2to3.pgen2 import token

def check_future_import(node):
    """If this is a future import, return set of symbols that are imported,
    else return None."""
    # node should be the import statement here
    if not (node.type == syms.simple_stmt and node.children):
        return set()
    node = node.children[0]
    # now node is the import_from node
    if not (node.type == syms.import_from and
            node.type == token.NAME and
            node.children[1].value == u'__future__'):
        return set()
    node = node.children[3]
    # now node is the import_as_name[s]
    print(python_grammar.number2symbol[node.type])
    if node.type == syms.import_as_names:
        result = set()
        for n in node.children:
            if n.type == token.NAME:
                result.add(n.value)
            elif n.type == syms.import_as_name:
                n = n.children[0]
                assert n.type == token.NAME
                result.add(n.value)
        return result
    elif node.type == syms.import_as_name:
        node = node.children[0]
        assert node.type == token.NAME
        return set([node.value])
    elif node.type == token.NAME:
        return set([node.value])
    else:
        assert 0, "strange import"

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
