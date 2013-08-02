u"""
Fixer for standard library imports renamed in Python 3
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, is_probably_builtin, Newline, does_tree_import
from lib2to3.pygram import python_symbols as syms
from lib2to3.pgen2 import token
from lib2to3.pytree import Node, Leaf

from ..fixer_util import NameImport

# used in simple_mapping_to_pattern()
MAPPING = {u"reprlib": u"repr",
           u"winreg": u"_winreg",
           u"configparser": u"ConfigParser",
           u"copyreg": u"copy_reg",
           u"queue": u"Queue",
           u"socketserver": u"SocketServer",
           u"_markupbase": u"markupbase",
           u"test.support": u"test.test_support",
           u"dbm.bsd": u"dbhash",
           u"dbm.ndbm": u"dbm",
           u"dbm.dumb": u"dumbdbm",
           u"dbm.gnu": u"gdbm",
           u"html.parser": u"HTMLParser",
           u"html.entities": u"htmlentitydefs",
           u"http.client": u"httplib",
           u"http.cookies": u"Cookie",
           u"http.cookiejar": u"cookielib",
#          "tkinter": "Tkinter",
           u"tkinter.dialog": u"Dialog",
           u"tkinter._fix": u"FixTk",
           u"tkinter.scrolledtext": u"ScrolledText",
           u"tkinter.tix": u"Tix",
           u"tkinter.constants": u"Tkconstants",
           u"tkinter.dnd": u"Tkdnd",
           u"tkinter.__init__": u"Tkinter",
           u"tkinter.colorchooser": u"tkColorChooser",
           u"tkinter.commondialog": u"tkCommonDialog",
           u"tkinter.font": u"tkFont",
           u"tkinter.messagebox": u"tkMessageBox",
           u"tkinter.turtle": u"turtle",
           u"urllib.robotparser": u"robotparser",
           u"xmlrpc.client": u"xmlrpclib",
           u"builtins": u"__builtin__",
}

# generic strings to help build patterns
# these variables mean (with http.client.HTTPConnection as an example):
# name = http
# attr = client
# used = HTTPConnection
# fmt_name is a formatted subpattern (simple_name_match or dotted_name_match)

# helps match 'queue', as in 'from queue import ...'
simple_name_match = u"name='%s'"
# helps match 'client', to be used if client has been imported from http
subname_match = u"attr='%s'"
# helps match 'http.client', as in 'import urllib.request'
dotted_name_match = u"dotted_name=dotted_name< %s '.' %s >"
# helps match 'queue', as in 'queue.Queue(...)'
power_onename_match = u"%s"
# helps match 'http.client', as in 'http.client.HTTPConnection(...)'
power_twoname_match = u"power< %s trailer< '.' %s > any* >"
# helps match 'client.HTTPConnection', if 'client' has been imported from http
power_subname_match = u"power< %s any* >"
# helps match 'from http.client import HTTPConnection'
from_import_match = u"from_import=import_from< 'from' %s 'import' imported=any >"
# helps match 'from http import client'
from_import_submod_match = u"from_import_submod=import_from< 'from' %s 'import' (%s | import_as_name< %s 'as' renamed=any > | import_as_names< any* (%s | import_as_name< %s 'as' renamed=any >) any* > ) >"
# helps match 'import urllib.request'
name_import_match = u"name_import=import_name< 'import' %s > | name_import=import_name< 'import' dotted_as_name< %s 'as' renamed=any > >"
# helps match 'import http.client, winreg'
multiple_name_import_match = u"name_import=import_name< 'import' dotted_as_names< names=any* > >"

def all_patterns(name):
    u"""
    Accepts a string and returns a pattern of possible patterns involving that name
    Called by simple_mapping_to_pattern for each name in the mapping it receives.
    """

    # i_ denotes an import-like node
    # u_ denotes a node that appears to be a usage of the name
    if u'.' in name:
        name, attr = name.split(u'.', 1)
        simple_name = simple_name_match % (name)
        simple_attr = subname_match % (attr)
        dotted_name = dotted_name_match % (simple_name, simple_attr)
        i_from = from_import_match % (dotted_name)
        i_from_submod = from_import_submod_match % (simple_name, simple_attr, simple_attr, simple_attr, simple_attr)
        i_name = name_import_match % (dotted_name, dotted_name)
        u_name = power_twoname_match % (simple_name, simple_attr)
        u_subname = power_subname_match % (simple_attr)
        return u' | \n'.join((i_name, i_from, i_from_submod, u_name, u_subname))
    else:
        simple_name = simple_name_match % (name)
        i_name = name_import_match % (simple_name, simple_name)
        i_from = from_import_match % (simple_name)
        u_name = power_onename_match % (simple_name)
        return u' | \n'.join((i_name, i_from, u_name))


class FixImports(fixer_base.BaseFix):

    PATTERN = u' | \n'.join([all_patterns(name) for name in MAPPING])
    PATTERN = u' | \n'.join((PATTERN, multiple_name_import_match))

    def fix_dotted_name(self, node, mapping=MAPPING):
        u"""
        Accepts either a DottedName node or a power node with a trailer.
        If mapping is given, use it; otherwise use our MAPPING
        Returns a node that can be in-place replaced by the node given
        """
        if node.type == syms.dotted_name:
            _name = node.children[0]
            _attr = node.children[2]
        elif node.type == syms.power:
            _name = node.children[0]
            _attr = node.children[1].children[1]
        name = _name.value
        attr = _attr.value
        full_name = name + u'.' + attr
        if not full_name in mapping:
            return
        to_repl = mapping[full_name]
        if u'.' in to_repl:
            repl_name, repl_attr = to_repl.split(u'.')
            _name.replace(Name(repl_name, prefix=_name.prefix))
            _attr.replace(Name(repl_attr, prefix=_attr.prefix))
        elif node.type == syms.dotted_name:
            node.replace(Name(to_repl, prefix=node.prefix))
        elif node.type == syms.power:
            _name.replace(Name(to_repl, prefix=_name.prefix))
            parent = _attr.parent
            _attr.remove()
            parent.remove()

    def fix_simple_name(self, node, mapping=MAPPING):
        u"""
        Accepts a Name leaf.
        If mapping is given, use it; otherwise use our MAPPING
        Returns a node that can be in-place replaced by the node given
        """
        assert node.type == token.NAME, repr(node)
        if not node.value in mapping:
            return
        replacement = mapping[node.value]
        node.replace(Leaf(token.NAME, unicode(replacement), prefix=node.prefix))

    def fix_submod_import(self, imported, name, node):
        u"""
        Accepts a list of NAME leafs, a name string, and a node
        node is given as an argument to BaseFix.transform()
        NAME leafs come from an import_as_names node (the children)
        name string is the base name found in node.
        """
        submods = []
        missed = []
        for attr in imported:
            dotted = u'.'.join((name, attr.value))
            if dotted in MAPPING:
                # get the replacement module
                to_repl = MAPPING[dotted]
                if u'.' not in to_repl:
                    # it's a simple name, so use a simple replacement.
                    _import = NameImport(Name(to_repl, prefix=u" "), attr.value)
                    submods.append(_import)
            elif attr.type == token.NAME:
                missed.append(attr.clone())
        if not submods:
            return

        parent = node.parent
        node.replace(submods[0])
        if len(submods) > 1:
            start = submods.pop(0)
            prev = start
            for submod in submods:
                parent.append_child(submod)
        if missed:
            self.warning(node, u"Imported names not known to 3to2 to be part of the package %s.  Leaving those alone... high probability that this code will be incorrect." % (name))
            children = [Name(u"from"), Name(name, prefix=u" "), Name(u"import", prefix=u" "), Node(syms.import_as_names, missed)]
            orig_stripped = Node(syms.import_from, children)
            parent.append_child(Newline())
            parent.append_child(orig_stripped)


    def get_dotted_import_replacement(self, name_node, attr_node, mapping=MAPPING, renamed=None):
        u"""
        For (http, client) given and httplib being the correct replacement,
        returns (httplib as client, None)
        For (test, support) given and test.test_support being the replacement,
        returns (test, test_support as support)
        """
        full_name = name_node.value + u'.' + attr_node.value
        replacement = mapping[full_name]
        if u'.' in replacement:
            new_name, new_attr = replacement.split(u'.')
            if renamed is None:
                return Name(new_name, prefix=name_node.prefix), Node(syms.dotted_as_name, [Name(new_attr, prefix=attr_node.prefix), Name(u'as', prefix=u" "), attr_node.clone()])
            else:
                return Name(new_name, prefix=name_node.prefix), Name(new_attr, prefix=attr_node.prefix)
        else:
            return Node(syms.dotted_as_name, [Name(replacement, prefix=name_node.prefix), Name(u'as', prefix=u' '), Name(attr_node.value, prefix=attr_node.prefix)]), None
    
    def transform(self, node, results):
        from_import = results.get(u"from_import")
        from_import_submod = results.get(u"from_import_submod")
        name_import = results.get(u"name_import")
        dotted_name = results.get(u"dotted_name")
        name = results.get(u"name")
        names = results.get(u"names")
        attr = results.get(u"attr")
        imported = results.get(u"imported")
        if names:
            for name in names:
                if name.type == token.NAME:
                    self.fix_simple_name(name)
                elif name.type == syms.dotted_as_name:
                    self.fix_simple_name(name.children[0]) if name.children[0].type == token.NAME else \
                    self.fix_dotted_name(name.children[0])
                elif name.type == syms.dotted_name:
                    self.fix_dotted_name(name)
        elif from_import_submod:
            renamed = results.get(u"renamed")
            new_name, new_attr = self.get_dotted_import_replacement(name, attr, renamed=renamed)
            if new_attr is not None:
                name.replace(new_name)
                attr.replace(new_attr)
            else:
                children = [Name(u"import"), new_name]
                node.replace(Node(syms.import_name, children, prefix=node.prefix))
        elif dotted_name:
            self.fix_dotted_name(dotted_name)
        elif name_import or from_import:
            self.fix_simple_name(name)
        elif name and not attr:
            if does_tree_import(None, MAPPING[name.value], node):
                self.fix_simple_name(name)
        elif name and attr:
            # Note that this will fix a dotted name that was never imported.  This will probably not matter.
            self.fix_dotted_name(node)
        elif imported and imported.type == syms.import_as_names:
            self.fix_submod_import(imported=imported.children, node=node, name=name.value)
