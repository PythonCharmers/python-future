u"""
Fixer for complicated imports
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, String, FromImport, Newline, Comma
from ..fixer_util import token, syms, Leaf, Node, Star, indentation, ImportAsName

TK_BASE_NAMES = (u'ACTIVE', u'ALL', u'ANCHOR', u'ARC',u'BASELINE', u'BEVEL', u'BOTH',
                 u'BOTTOM', u'BROWSE', u'BUTT', u'CASCADE', u'CENTER', u'CHAR',
                 u'CHECKBUTTON', u'CHORD', u'COMMAND', u'CURRENT', u'DISABLED',
                 u'DOTBOX', u'E', u'END', u'EW', u'EXCEPTION', u'EXTENDED', u'FALSE',
                 u'FIRST', u'FLAT', u'GROOVE', u'HIDDEN', u'HORIZONTAL', u'INSERT',
                 u'INSIDE', u'LAST', u'LEFT', u'MITER', u'MOVETO', u'MULTIPLE', u'N',
                 u'NE', u'NO', u'NONE', u'NORMAL', u'NS', u'NSEW', u'NUMERIC', u'NW',
                 u'OFF', u'ON', u'OUTSIDE', u'PAGES', u'PIESLICE', u'PROJECTING',
                 u'RADIOBUTTON', u'RAISED', u'READABLE', u'RIDGE', u'RIGHT',
                 u'ROUND', u'S', u'SCROLL', u'SE', u'SEL', u'SEL_FIRST', u'SEL_LAST',
                 u'SEPARATOR', u'SINGLE', u'SOLID', u'SUNKEN', u'SW', u'StringTypes',
                 u'TOP', u'TRUE', u'TclVersion', u'TkVersion', u'UNDERLINE', 
                 u'UNITS', u'VERTICAL', u'W', u'WORD', u'WRITABLE', u'X', u'Y', u'YES',
                 u'wantobjects')

PY2MODULES = { 
              u'urllib2' : (
                  u'AbstractBasicAuthHandler', u'AbstractDigestAuthHandler',
                  u'AbstractHTTPHandler', u'BaseHandler', u'CacheFTPHandler',
                  u'FTPHandler', u'FileHandler', u'HTTPBasicAuthHandler',
                  u'HTTPCookieProcessor', u'HTTPDefaultErrorHandler',
                  u'HTTPDigestAuthHandler', u'HTTPError', u'HTTPErrorProcessor',
                  u'HTTPHandler', u'HTTPPasswordMgr',
                  u'HTTPPasswordMgrWithDefaultRealm', u'HTTPRedirectHandler',
                  u'HTTPSHandler', u'OpenerDirector', u'ProxyBasicAuthHandler',
                  u'ProxyDigestAuthHandler', u'ProxyHandler', u'Request',
                  u'StringIO', u'URLError', u'UnknownHandler', u'addinfourl',
                  u'build_opener', u'install_opener', u'parse_http_list',
                  u'parse_keqv_list', u'randombytes', u'request_host', u'urlopen'),
              u'urllib' : (
                  u'ContentTooShortError', u'FancyURLopener',u'URLopener',
                  u'basejoin', u'ftperrors', u'getproxies',
                  u'getproxies_environment', u'localhost', u'pathname2url',
                  u'quote', u'quote_plus', u'splitattr', u'splithost',
                  u'splitnport', u'splitpasswd', u'splitport', u'splitquery',
                  u'splittag', u'splittype', u'splituser', u'splitvalue',
                  u'thishost', u'unquote', u'unquote_plus', u'unwrap',
                  u'url2pathname', u'urlcleanup', u'urlencode', u'urlopen',
                  u'urlretrieve',),
              u'urlparse' : (
                  u'parse_qs', u'parse_qsl', u'urldefrag', u'urljoin',
                  u'urlparse', u'urlsplit', u'urlunparse', u'urlunsplit'),
              u'dbm' : (
                  u'ndbm', u'gnu', u'dumb'),
              u'anydbm' : (
                  u'error', u'open'),
              u'whichdb' : (
                  u'whichdb',),
              u'BaseHTTPServer' : (
                  u'BaseHTTPRequestHandler', u'HTTPServer'),
              u'CGIHTTPServer' : (
                  u'CGIHTTPRequestHandler',),
              u'SimpleHTTPServer' : (
                  u'SimpleHTTPRequestHandler',),
              u'FileDialog' : TK_BASE_NAMES + (
                  u'FileDialog', u'LoadFileDialog', u'SaveFileDialog',
                  u'dialogstates', u'test'),
              u'tkFileDialog' : (
                  u'Directory', u'Open', u'SaveAs', u'_Dialog', u'askdirectory',
                  u'askopenfile', u'askopenfilename', u'askopenfilenames',
                  u'askopenfiles', u'asksaveasfile', u'asksaveasfilename'),
              u'SimpleDialog' : TK_BASE_NAMES + (
                  u'SimpleDialog',),
              u'tkSimpleDialog' : TK_BASE_NAMES + (
                  u'askfloat', u'askinteger', u'askstring', u'Dialog'),
              u'SimpleXMLRPCServer' : (
                  u'CGIXMLRPCRequestHandler', u'SimpleXMLRPCDispatcher',
                  u'SimpleXMLRPCRequestHandler', u'SimpleXMLRPCServer',
                  u'list_public_methods', u'remove_duplicates',
                  u'resolve_dotted_attribute'),
              u'DocXMLRPCServer' : (
                  u'DocCGIXMLRPCRequestHandler', u'DocXMLRPCRequestHandler',
                  u'DocXMLRPCServer', u'ServerHTMLDoc',u'XMLRPCDocGenerator'),
                }

MAPPING = { u'urllib.request' :
                (u'urllib2', u'urllib'),
            u'urllib.error' :
                (u'urllib2', u'urllib'),
            u'urllib.parse' :
                (u'urllib2', u'urllib', u'urlparse'),
            u'dbm.__init__' :
                (u'anydbm', u'whichdb'),
            u'http.server' :
                (u'CGIHTTPServer', u'SimpleHTTPServer', u'BaseHTTPServer'),
            u'tkinter.filedialog' :
                (u'tkFileDialog', u'FileDialog'),
            u'tkinter.simpledialog' :
                (u'tkSimpleDialog', u'SimpleDialog'),
            u'xmlrpc.server' :
                (u'DocXMLRPCServer', u'SimpleXMLRPCServer'),
            }

# helps match 'http', as in 'from http.server import ...'
simple_name = u"name='%s'"
# helps match 'server', as in 'from http.server import ...'
simple_attr = u"attr='%s'"
# helps match 'HTTPServer', as in 'from http.server import HTTPServer'
simple_using = u"using='%s'"
# helps match 'urllib.request', as in 'import urllib.request'
dotted_name = u"dotted_name=dotted_name< %s '.' %s >"
# helps match 'http.server', as in 'http.server.HTTPServer(...)'
power_twoname = u"pow=power< %s trailer< '.' %s > trailer< '.' using=any > any* >"
# helps match 'dbm.whichdb', as in 'dbm.whichdb(...)'
power_onename = u"pow=power< %s trailer< '.' using=any > any* >"
# helps match 'from http.server import HTTPServer'
# also helps match 'from http.server import HTTPServer, SimpleHTTPRequestHandler'
# also helps match 'from http.server import *'
from_import = u"from_import=import_from< 'from' %s 'import' (import_as_name< using=any 'as' renamed=any> | in_list=import_as_names< using=any* > | using='*' | using=NAME) >"
# helps match 'import urllib.request'
name_import = u"name_import=import_name< 'import' (%s | in_list=dotted_as_names< imp_list=any* >) >"

#############
# WON'T FIX #
#############

# helps match 'import urllib.request as name'
name_import_rename = u"name_import_rename=dotted_as_name< %s 'as' renamed=any >"
# helps match 'from http import server'
from_import_rename = u"from_import_rename=import_from< 'from' %s 'import' (%s | import_as_name< %s 'as' renamed=any > | in_list=import_as_names< any* (%s | import_as_name< %s 'as' renamed=any >) any* >) >"

def all_modules_subpattern():
    u"""
    Builds a pattern for all toplevel names
    (urllib, http, etc)
    """
    names_dot_attrs = [mod.split(u".") for mod in MAPPING]
    ret = u"( " + u" | ".join([dotted_name % (simple_name % (mod[0]),
                                            simple_attr % (mod[1])) for mod in names_dot_attrs])
    ret += u" | "
    ret += u" | ".join([simple_name % (mod[0]) for mod in names_dot_attrs if mod[1] == u"__init__"]) + u" )"
    return ret

def all_candidates(name, attr, MAPPING=MAPPING):
    u"""
    Returns all candidate packages for the name.attr
    """
    dotted = name + u'.' + attr
    assert dotted in MAPPING, u"No matching package found."
    ret = MAPPING[dotted]
    if attr == u'__init__':
        return ret + (name,)
    return ret

def new_package(name, attr, using, MAPPING=MAPPING, PY2MODULES=PY2MODULES):
    u"""
    Returns which candidate package for name.attr provides using
    """
    for candidate in all_candidates(name, attr, MAPPING):
        if using in PY2MODULES[candidate]:
            break
    else:
        candidate = None

    return candidate

def build_import_pattern(mapping1, mapping2):
    u"""
    mapping1: A dict mapping py3k modules to all possible py2k replacements
    mapping2: A dict mapping py2k modules to the things they do
    This builds a HUGE pattern to match all ways that things can be imported
    """
    # py3k: urllib.request, py2k: ('urllib2', 'urllib')
    yield from_import % (all_modules_subpattern())
    for py3k, py2k in mapping1.items():
        name, attr = py3k.split(u'.')
        s_name = simple_name % (name)
        s_attr = simple_attr % (attr)
        d_name = dotted_name % (s_name, s_attr)
        yield name_import % (d_name)
        yield power_twoname % (s_name, s_attr)
        if attr == u'__init__':
            yield name_import % (s_name)
            yield power_onename % (s_name)
        yield name_import_rename % (d_name)
        yield from_import_rename % (s_name, s_attr, s_attr, s_attr, s_attr)

def name_import_replacement(name, attr):
    children = [Name(u"import")]
    for c in all_candidates(name.value, attr.value):
        children.append(Name(c, prefix=u" "))
        children.append(Comma())
    children.pop()
    replacement = Node(syms.import_name, children)
    return replacement


class FixImports2(fixer_base.BaseFix):

    run_order = 4

    PATTERN = u" | \n".join(build_import_pattern(MAPPING, PY2MODULES))

    def transform(self, node, results):
        # The patterns dictate which of these names will be defined
        name = results.get(u"name")
        attr = results.get(u"attr")
        if attr is None:
            attr = Name(u"__init__")
        using = results.get(u"using")
        in_list = results.get(u"in_list")
        imp_list = results.get(u"imp_list")
        power = results.get(u"pow")
        before = results.get(u"before")
        after = results.get(u"after")
        d_name = results.get(u"dotted_name")
        # An import_stmt is always contained within a simple_stmt
        simple_stmt = node.parent
        # The parent is useful for adding new import_stmts
        parent = simple_stmt.parent
        idx = parent.children.index(simple_stmt)
        if any((results.get(u"from_import_rename") is not None,
                results.get(u"name_import_rename") is not None)): 
            self.cannot_convert(node, reason=u"ambiguity: import binds a single name")

        elif using is None and not in_list:
            # import urllib.request, single-name import
            replacement = name_import_replacement(name, attr)
            replacement.prefix = node.prefix
            node.replace(replacement)

        elif using is None:
            # import ..., urllib.request, math, http.sever, ...
            for d_name in imp_list:
                if d_name.type == syms.dotted_name:
                    name = d_name.children[0]
                    attr = d_name.children[2]
                elif d_name.type == token.NAME and d_name.value + u".__init__" in MAPPING:
                    name = d_name
                    attr = Name(u"__init__")
                else:
                    continue
                if name.value + u"." + attr.value not in MAPPING:
                    continue
                candidates = all_candidates(name.value, attr.value)
                children = [Name(u"import")]
                for c in candidates:
                    children.append(Name(c, prefix=u" "))
                    children.append(Comma())
                children.pop()
                # Put in the new statement.
                indent = indentation(simple_stmt)
                next_stmt = Node(syms.simple_stmt, [Node(syms.import_name, children), Newline()])
                parent.insert_child(idx+1, next_stmt)
                parent.insert_child(idx+1, Leaf(token.INDENT, indent))
                # Remove the old imported name
                test_comma = d_name.next_sibling
                if test_comma and test_comma.type == token.COMMA:
                    test_comma.remove()
                elif test_comma is None:
                    test_comma = d_name.prev_sibling
                    if test_comma and test_comma.type == token.COMMA:
                        test_comma.remove()
                d_name.remove()
            if not in_list.children:
                simple_stmt.remove()

        elif in_list is not None:
            ##########################################################
            # "from urllib.request import urlopen, urlretrieve, ..." #
            # Replace one import statement with potentially many.    #
            ##########################################################
            packages = dict([(n,[]) for n in all_candidates(name.value,
                                                            attr.value)])
            # Figure out what names need to be imported from what
            # Add them to a dict to be parsed once we're completely done
            for imported in using:
                if imported.type == token.COMMA:
                    continue
                if imported.type == syms.import_as_name:
                    test_name = imported.children[0].value
                    if len(imported.children) > 2:
                        # 'as' whatever
                        rename = imported.children[2].value
                    else:
                        rename = None
                elif imported.type == token.NAME:
                    test_name = imported.value
                    rename = None
                pkg = new_package(name.value, attr.value, test_name)
                packages[pkg].append((test_name, rename))

            # Parse the dict to create new import statements to replace this one
            imports = []
            for new_pkg, names in packages.items():
                if not names:
                    # Didn't import anything from that package, move along
                    continue
                new_names = []
                for test_name, rename in names:
                    if rename is None:
                        new_names.append(Name(test_name, prefix=u" "))
                    else:
                        new_names.append(ImportAsName(test_name, rename, prefix=u" "))
                    new_names.append(Comma())
                new_names.pop()
                imports.append(FromImport(new_pkg, new_names))
            # Replace this import statement with one of the others
            replacement = imports.pop()
            replacement.prefix = node.prefix
            node.replace(replacement)
            indent = indentation(simple_stmt)
            # Add the remainder of the imports as new statements.
            while imports:
                next_stmt = Node(syms.simple_stmt, [imports.pop(), Newline()])
                parent.insert_child(idx+1, next_stmt)
                parent.insert_child(idx+1, Leaf(token.INDENT, indent))

        elif using.type == token.STAR:
            # from urllib.request import *
            nodes = [FromImport(pkg, [Star(prefix=u" ")]) for pkg in
                                        all_candidates(name.value, attr.value)]
            replacement = nodes.pop()
            replacement.prefix = node.prefix
            node.replace(replacement)
            indent = indentation(simple_stmt)
            while nodes:
                next_stmt = Node(syms.simple_stmt, [nodes.pop(), Newline()])
                parent.insert_child(idx+1, next_stmt)
                parent.insert_child(idx+1, Leaf(token.INDENT, indent))
        elif power is not None:
            # urllib.request.urlopen
            # Replace it with urllib2.urlopen
            pkg = new_package(name.value, attr.value, using.value)
            # Remove the trailer node that contains attr.
            if attr.parent:
                attr.parent.remove()
            name.replace(Name(pkg, prefix=name.prefix))

        elif using.type == token.NAME:
            # from urllib.request import urlopen
            pkg = new_package(name.value, attr.value, using.value)
            if attr.value == u"__init__" and pkg == name.value:
                # Replacing "from abc import xyz" with "from abc import xyz"
                # Just leave it alone so as not to mess with other fixers
                return
            else:
                node.replace(FromImport(pkg, [using]))
