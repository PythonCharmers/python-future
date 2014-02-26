"""
Python 3 reorganized the standard library (PEP 3108). This module exposes
several standard library modules to Python 2 under their new Python 3
names.

It is designed to be used as follows::

    from future import standard_library
    standard_library.install_hooks()

And then these normal Py3 imports work on both Py3 and Py2::

    import builtins
    import configparser
    import copyreg
    import queue
    import reprlib
    import socketserver
    import winreg    # on Windows only
    import test.support
    import html, html.parser, html.entites
    import http, http.client, http.server
    import _thread
    import _dummythread
    import _markupbase

    from itertools import filterfalse, zip_longest
    from sys import intern
    
(The renamed modules and functions are still available under their old
names on Python 2.)

To turn off the import hooks, use::

    standard_library.remove_hooks()

and to turn it on again, use::

    standard_library.install_hooks()

This is a cleaner alternative to this idiom (see
http://docs.pythonsprints.com/python3_porting/py-porting.html)::

    try:
        import queue
    except ImportError:
        import Queue as queue


Limitations
-----------
We don't currently support these modules, but would like to::

    import http.cookies, http.cookiejar
    import dbm
    import dbm.dumb
    import dbm.gnu
    import xmlrpc.client
    import collections.abc  # on Py33
    import urllib.request
    import urllib.parse
    import urllib.error
    import urllib.robotparser
    import tkinter
    import pickle     # should (optionally) bring in cPickle on Python 2


Notes
-----
This module only supports Python 2.6, Python 2.7, and Python 3.1+.

The following renames are already supported on Python 2.7 without any
additional work from us::
    
    reload() -> imp.reload()
    reduce() -> functools.reduce()
    StringIO.StringIO -> io.StringIO
    Bytes.BytesIO -> io.BytesIO

Old things that can one day be fixed automatically by futurize.py::

  string.uppercase -> string.ascii_uppercase   # works on either Py2.7 or Py3+
  sys.maxint -> sys.maxsize      # but this isn't identical

TODO: Check out these:
Not available on Py2.6:
  unittest2 -> unittest?
  buffer -> memoryview?

"""

from __future__ import absolute_import

import sys
import logging
import imp
import contextlib
import types
import copy
import os

from future import utils

# The modules that are defined under the same names on Py3 but with
# different contents in a significant way (e.g. submodules) are:
#   pickle (fast one)
#   dbm
#   urllib
#   test

# These ones are new (i.e. no problem)
#   http
#   html
#   tkinter
#   xmlrpc

# These modules need names from elsewhere being added to them:
#   subprocess: should provide getoutput and other fns from commands
#               module but these fns are missing: getstatus, mk2arg,
#               mkarg

# Old to new
# etc: see lib2to3/fixes/fix_imports.py
RENAMES = {
           # 'cStringIO': 'io',  # there's a new io module in Python 2.6
                                 # that provides StringIO and BytesIO
           # 'StringIO': 'io',   # ditto
           # 'cPickle': 'pickle',
           '__builtin__': 'builtins',
           'copy_reg': 'copyreg',
           'Queue': 'queue',
           'future.standard_library.socketserver': 'socketserver',
           'ConfigParser': 'configparser',
           'repr': 'reprlib',
           # 'FileDialog': 'tkinter.filedialog',
           # 'tkFileDialog': 'tkinter.filedialog',
           # 'SimpleDialog': 'tkinter.simpledialog',
           # 'tkSimpleDialog': 'tkinter.simpledialog',
           # 'tkColorChooser': 'tkinter.colorchooser',
           # 'tkCommonDialog': 'tkinter.commondialog',
           # 'Dialog': 'tkinter.dialog',
           # 'Tkdnd': 'tkinter.dnd',
           # 'tkFont': 'tkinter.font',
           # 'tkMessageBox': 'tkinter.messagebox',
           # 'ScrolledText': 'tkinter.scrolledtext',
           # 'Tkconstants': 'tkinter.constants',
           # 'Tix': 'tkinter.tix',
           # 'ttk': 'tkinter.ttk',
           # 'Tkinter': 'tkinter',
           '_winreg': 'winreg',
           'thread': '_thread',
           'dummy_thread': '_dummy_thread',
           # 'anydbm': 'dbm',   # causes infinite import loop 
           # 'whichdb': 'dbm',  # causes infinite import loop 
           # anydbm and whichdb are handled by fix_imports2
           # 'dbhash': 'dbm.bsd',
           # 'dumbdbm': 'dbm.dumb',
           # 'dbm': 'dbm.ndbm',
           # 'gdbm': 'dbm.gnu',
           # 'xmlrpclib': 'xmlrpc.client',
           # 'DocXMLRPCServer': 'xmlrpc.server',
           # 'SimpleXMLRPCServer': 'xmlrpc.server',
           # 'httplib': 'http.client',
           # 'htmlentitydefs' : 'html.entities',
           # 'HTMLParser' : 'html.parser',
           # 'Cookie': 'http.cookies',
           # 'cookielib': 'http.cookiejar',
           # 'BaseHTTPServer': 'http.server',
           # 'SimpleHTTPServer': 'http.server',
           # 'CGIHTTPServer': 'http.server',
           'future.standard_library.test': 'test',  # primarily for renaming test_support to support
           # 'commands': 'subprocess',
           # 'urlparse' : 'urllib.parse',
           # 'robotparser' : 'urllib.robotparser',
           # 'abc': 'collections.abc',   # for Py33
           'future.standard_library.html': 'html',
           'future.standard_library.http': 'http',
           # 'future.standard_library.urllib': 'newurllib',
           'future.standard_library._markupbase': '_markupbase',
          }


REPLACED_MODULES = set(['test', 'urllib', 'pickle'])  # add dbm when we support it
# These are entirely new to Python 2.x, so they cause no potential clashes
#   xmlrpc, tkinter, http, html


class WarnOnImport(object):
    def __init__(self, *args):
        self.module_names = args
 
    def find_module(self, fullname, path=None):
        if fullname in self.module_names:
            self.path = path
            return self
        return None
 
    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]
        module_info = imp.find_module(name, self.path)
        module = imp.load_module(name, *module_info)
        sys.modules[name] = module
 
        logging.warning("Imported deprecated module %s", name)
        return module


class RenameImport(object):
    """
    A class for import hooks mapping Py3 module names etc. to the Py2 equivalents.
    """
    # Different RenameImport classes are created when importing this module from
    # different source files. This causes isinstance(hook, RenameImport) checks
    # to produce inconsistent results. We add this RENAMER attribute here so
    # remove_hooks() and install_hooks() can find instances of these classes
    # easily:
    RENAMER = True

    def __init__(self, old_to_new):
        '''
        Pass in a dictionary-like object mapping from old names to new
        names. E.g. {'ConfigParser': 'configparser', 'cPickle': 'pickle'}
        '''
        self.old_to_new = old_to_new
        both = set(old_to_new.keys()) & set(old_to_new.values())
        assert (len(both) == 0 and
                len(set(old_to_new.values())) == len(old_to_new.values())), \
               'Ambiguity in renaming (handler not implemented)'
        self.new_to_old = dict((new, old) for (old, new) in old_to_new.items())
 
    def find_module(self, fullname, path=None):
        # Handles hierarchical importing: package.module.module2
        new_base_names = set([s.split('.')[0] for s in self.new_to_old])
        if fullname in set(self.old_to_new) | new_base_names:
            return self
        return None
 
    def load_module(self, name):
        path = None
        if name in sys.modules:
            return sys.modules[name]
        elif name in self.new_to_old:
            # New name. Look up the corresponding old (Py2) name:
            name = self.new_to_old[name]
        # Was: with suspend_hooks():
        #          module = self._find_and_load_module(name)
        module = self._find_and_load_module(name)
        sys.modules[name] = module
        return module
 
    def _find_and_load_module(self, name, path=None):
        """
        Finds and loads it. But if there's a . in the name, handles it
        properly.
        """
        bits = name.split('.')
        while len(bits) > 1:
            # Treat the first bit as a package
            packagename = bits.pop(0)
            package = self._find_and_load_module(packagename, path)
            try:
                path = package.__path__
            except AttributeError:
                logging.debug('Debug me: no __path__. '
                              'Should anything special be done here?')
                pass
            # if packagename == 'future':
            #     path = FIXME
        name = bits[0]
        if name == 'moves':
            # imp.find_module doesn't find this fake module
            return moves
        else:
            module_info = imp.find_module(name, path)
            return imp.load_module(name, *module_info)


# (New module name, new object name, old module name, old object name)
MOVES = [('collections', 'UserList', 'UserList', 'UserList'),
         ('collections', 'UserDict', 'UserDict', 'UserDict'),
         ('collections', 'UserString','UserString', 'UserString'),
         ('itertools', 'filterfalse','itertools', 'ifilterfalse'),
         ('itertools', 'zip_longest','itertools', 'izip_longest'),
         ('sys', 'intern','__builtin__', 'intern'),
         # urllib._urlopener	urllib.request
         # urllib.ContentTooShortError	urllib.error
         # urllib.FancyURLOpener	urllib.request
         # urllib.pathname2url	urllib.request
         # urllib.quote	urllib.parse
         # urllib.quote_plus	urllib.parse
         # urllib.splitattr	urllib.parse
         # urllib.splithost	urllib.parse
         # urllib.splitnport	urllib.parse
         # urllib.splitpasswd	urllib.parse
         # urllib.splitport	urllib.parse
         # urllib.splitquery	urllib.parse
         # urllib.splittag	urllib.parse
         # urllib.splittype	urllib.parse
         # urllib.splituser	urllib.parse
         # urllib.splitvalue	urllib.parse
         # urllib.unquote	urllib.parse
         # urllib.unquote_plus	urllib.parse
         # urllib.urlcleanup	urllib.request
         # urllib.urlencode	urllib.parse
         # urllib.urlopen	urllib.request
         # urllib.URLOpener	urllib.request
         # urllib.urlretrieve	urllib.request
         # urllib2.AbstractBasicAuthHandler	urllib.request
         # urllib2.AbstractDigestAuthHandler	urllib.request
         # urllib2.BaseHandler	urllib.request
         # urllib2.build_opener	urllib.request
         # urllib2.CacheFTPHandler	urllib.request
         # urllib2.FileHandler	urllib.request
         # urllib2.FTPHandler	urllib.request
         # urllib2.HTTPBasicAuthHandler	urllib.request
         # urllib2.HTTPCookieProcessor	urllib.request
         # urllib2.HTTPDefaultErrorHandler	urllib.request
         # urllib2.HTTPDigestAuthHandler	urllib.request
         # urllib2.HTTPError	urllib.request
         # urllib2.HTTPHandler	urllib.request
         # urllib2.HTTPPasswordMgr	urllib.request
         # urllib2.HTTPPasswordMgrWithDefaultRealm	urllib.request
         # urllib2.HTTPRedirectHandler	urllib.request
         # urllib2.HTTPSHandler	urllib.request
         # urllib2.install_opener	urllib.request
         # urllib2.OpenerDirector	urllib.request
         # urllib2.ProxyBasicAuthHandler	urllib.request
         # urllib2.ProxyDigestAuthHandler	urllib.request
         # urllib2.ProxyHandler	urllib.request
         # urllib2.Request	urllib.request
         # urllib2.UnknownHandler	urllib.request
         # urllib2.URLError	urllib.request
         # urllib2.urlopen	urllib.request
         # urlparse.parse_qs	urllib.parse
         # urlparse.parse_qsl	urllib.parse
         # urlparse.urldefrag	urllib.parse
         # urlparse.urljoin	urllib.parse
         # urlparse.urlparse	urllib.parse
         # urlparse.urlsplit	urllib.parse
         # urlparse.urlunparse	urllib.parse
         # urlparse.urlunsplit	urllib.parse
        ]


class hooks(object):
    """
    Acts as a context manager. Saves the state of sys.modules and restores it
    after the 'with' block. 
    
    Use like this:
    
    >>> from future import standard_library
    >>> with standard_library.hooks():
    ...     import http.client
    >>> import requests     # incompatible with ``future``'s standard library hooks

    For this to work, http.client will be scrubbed from sys.modules after the
    'with' block. That way the modules imported in the 'with' block will
    continue to be accessible in the current namespace but not from any
    imported modules (like requests).
    """
    def __enter__(self):
        logging.debug('Entering hooks context manager')
        self.old_sys_modules = copy.copy(sys.modules)
        self.hooks_were_installed = detect_hooks()
        scrub_py2_stdlib_modules()
        install_hooks()
        return self

    def __exit__(self, *args):
        logging.debug('Exiting hooks context manager')
        if not self.hooks_were_installed:
            # Reset sys.modules to how it was at the start.
            sys.modules = self.old_sys_modules
            remove_hooks()
            scrub_future_stdlib_modules()


def is_future_stdlib_module(m):
    """
    Returns True if the module m is provided by the future.standard_library
    package.
    """


def is_py2_stdlib_module(m):
    """
    Tries to infer whether the module m is from the Python 2 standard library.
    This may not be reliable on all systems.
    """
    if not 'stdlib_path' in is_py2_stdlib_module.__dict__:
        stdlib_files = [contextlib.__file__, os.__file__, copy.__file__]
        stdlib_paths = [os.path.split(f)[0] for f in stdlib_files]
        if not len(set(stdlib_paths)) == 1:
            raise RuntimeError('Could not determine the location of the Python '
                               'standard library')
        # They are identical, so choose one and add / so we don't match urllib2
        is_py2_stdlib_module.stdlib_path = stdlib_paths[0] + os.sep

    if m.__name__ in sys.builtin_module_names:
        return True

    if (hasattr(m, '__file__') and
        os.path.split(m.__file__)[0].startswith(is_py2_stdlib_module.stdlib_path)):
        return True
        
    return False


def scrub_py2_stdlib_modules():
    """
    Removes any Python 2 standard library modules from ``sys.modules`` that 

    # Was: ... that do not exist under the same names in the Python 3 standard library.
    
    These modules may interfere with importing future.standard_library modules
    with similar names (e.g. urllib) using the import hooks.
    """
    for modulename in REPLACED_MODULES:
        if not modulename in sys.modules:
            continue

        module = sys.modules[modulename]

        if is_py2_stdlib_module(module):
            logging.warn('Deleting {} from sys.modules'.format(modulename))
            del sys.modules[modulename]


def scrub_future_stdlib_modules():
    """
    Removes any submodules of ``future.standard_library`` from sys.modules.
    """
    future_stdlib = os.path.join('future', 'standard_library')
    for modulename, module in sys.modules.items():
        if modulename not in ['standard_library', 'future.standard_library']:
            if (hasattr(module, '__file__') and
                module.__file__.startswith(future_stdlib)):
                logging.warn('Deleting {} from sys.modules'.format(modulename))
                del sys.modules[modulename]


class suspend_hooks(object):
    """
    Acts as a context manager. Use like this:
    
    >>> from future import standard_library
    >>> standard_library.install_hooks()
    >>> import http.client
    >>> # ...
    >>> with standard_library.suspend_hooks():
    >>>     import requests     # incompatible with ``future``'s standard library hooks

    If the hooks were disabled before the context, they are not installed when
    the context is left.
    """
    def __enter__(self):
        self.hooks_were_installed = detect_hooks()
        remove_hooks()
        scrub_future_stdlib_modules()
        return self
    def __exit__(self, *args):
        if self.hooks_were_installed:
            scrub_py2_stdlib_modules()    # in case they interfere ... e.g. urllib
            install_hooks()
            # TODO: add the scrubbed modules back to the sys.modules cache?


def install_hooks():
    if utils.PY3:
        return
    logging.debug('sys.meta_path was: {}'.format(sys.meta_path))
    logging.debug('Installing hooks ...')

    for (newmodname, newobjname, oldmodname, oldobjname) in MOVES:
        newmod = __import__(newmodname)
        oldmod = __import__(oldmodname)
        obj = getattr(oldmod, oldobjname)
        setattr(newmod, newobjname, obj)

    # Add it unless it's there already
    newhook = RenameImport(RENAMES)
    if not detect_hooks():
        sys.meta_path.append(newhook)
    logging.debug('sys.meta_path is now: {}'.format(sys.meta_path))


def enable_hooks():
    """
    Deprecated. Use install_hooks() instead. This will be removed by
    ``future`` v1.0.
    """
    install_hooks()


def remove_hooks():
    """
    Use to remove the ``future.standard_library`` import hooks.
    """
    if utils.PY3:
        return
    logging.debug('Uninstalling hooks ...')
    # Loop backwards, so deleting items keeps the ordering:
    for i, hook in list(enumerate(sys.meta_path))[::-1]:
        if hasattr(hook, 'RENAMER'):
            del sys.meta_path[i]


def disable_hooks():
    """
    Deprecated. Use remove_hooks() instead. This will be removed by
    ``future`` v1.0.
    """
    remove_hooks()


def detect_hooks():
    """
    Returns True if the import hooks are installed, False if not.
    """
    logging.debug('Detecting hooks ...')
    present = any([hasattr(hook, 'RENAMER') for hook in sys.meta_path])
    if present:
        logging.debug('Detected.')
    else:
        logging.debug('Not detected.')
    return present


# Now import the modules:
# with hooks():
#     for (oldname, newname) in RENAMES.items():
#         if newname == 'winreg' and sys.platform not in ['win32', 'win64']:
#             continue
#         if newname in REPLACED_MODULES:
#             # Skip this check for e.g. the stdlib's ``test`` module,
#             # which we have replaced completely.
#             continue
#         newmod = __import__(newname)
#         globals()[newname] = newmod


### Pasted from six.py v1.5.2 by Benjamin Peterson ###
def _add_doc(func, doc):
    """Add documentation to a function."""
    func.__doc__ = doc


def _import_module(name):
    """Import module, returning the module after the last dot."""
    __import__(name)
    return sys.modules[name]


class _LazyDescr(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, tp):
        result = self._resolve()
        setattr(obj, self.name, result) # Invokes __set__.
        # This is a bit ugly, but it avoids running this again.
        delattr(obj.__class__, self.name)
        return result


class MovedModule(_LazyDescr):

    def __init__(self, name, old, new=None):
        super(MovedModule, self).__init__(name)
        if utils.PY3:
            if new is None:
                new = name
            self.mod = new
        else:
            self.mod = old

    def _resolve(self):
        return _import_module(self.mod)

    def __getattr__(self, attr):
        # Hack around the Django autoreloader. The reloader tries to get
        # __file__ or __name__ of every module in sys.modules. This doesn't work
        # well if this MovedModule is for an module that is unavailable on this
        # machine (like winreg on Unix systems). Thus, we pretend __file__ and
        # __name__ don't exist if the module hasn't been loaded yet. See issues
        # #51 and #53.
        if attr in ("__file__", "__name__") and self.mod not in sys.modules:
            raise AttributeError
        _module = self._resolve()
        value = getattr(_module, attr)
        setattr(self, attr, value)
        return value


class _LazyModule(types.ModuleType):

    def __init__(self, name):
        super(_LazyModule, self).__init__(name)
        self.__doc__ = self.__class__.__doc__

    def __dir__(self):
        attrs = ["__doc__", "__name__"]
        attrs += [attr.name for attr in self._moved_attributes]
        return attrs

    # Subclasses should override this
    _moved_attributes = []


class MovedAttribute(_LazyDescr):

    def __init__(self, name, old_mod, new_mod, old_attr=None, new_attr=None):
        super(MovedAttribute, self).__init__(name)
        if utils.PY3:
            if new_mod is None:
                new_mod = name
            self.mod = new_mod
            if new_attr is None:
                if old_attr is None:
                    new_attr = name
                else:
                    new_attr = old_attr
            self.attr = new_attr
        else:
            self.mod = old_mod
            if old_attr is None:
                old_attr = name
            self.attr = old_attr

    def _resolve(self):
        module = _import_module(self.mod)
        return getattr(module, self.attr)



class _MovedItems(_LazyModule):
    """Lazy loading of moved objects"""


_moved_attributes = [
    MovedAttribute("cStringIO", "cStringIO", "io", "StringIO"),
    MovedAttribute("filter", "itertools", "builtins", "ifilter", "filter"),
    MovedAttribute("filterfalse", "itertools", "itertools", "ifilterfalse", "filterfalse"),
    MovedAttribute("input", "__builtin__", "builtins", "raw_input", "input"),
    MovedAttribute("map", "itertools", "builtins", "imap", "map"),
    MovedAttribute("range", "__builtin__", "builtins", "xrange", "range"),
    MovedAttribute("reload_module", "__builtin__", "imp", "reload"),
    MovedAttribute("reduce", "__builtin__", "functools"),
    MovedAttribute("StringIO", "StringIO", "io"),
    MovedAttribute("UserString", "UserString", "collections"),
    MovedAttribute("xrange", "__builtin__", "builtins", "xrange", "range"),
    MovedAttribute("zip", "itertools", "builtins", "izip", "zip"),
    MovedAttribute("zip_longest", "itertools", "itertools", "izip_longest", "zip_longest"),

    MovedModule("builtins", "__builtin__"),
    MovedModule("configparser", "ConfigParser"),
    MovedModule("copyreg", "copy_reg"),
    MovedModule("dbm_gnu", "gdbm", "dbm.gnu"),
    MovedModule("http_cookiejar", "cookielib", "http.cookiejar"),
    MovedModule("http_cookies", "Cookie", "http.cookies"),
    MovedModule("html_entities", "htmlentitydefs", "html.entities"),
    MovedModule("html_parser", "HTMLParser", "html.parser"),
    MovedModule("http_client", "httplib", "http.client"),
    MovedModule("email_mime_multipart", "email.MIMEMultipart", "email.mime.multipart"),
    MovedModule("email_mime_text", "email.MIMEText", "email.mime.text"),
    MovedModule("email_mime_base", "email.MIMEBase", "email.mime.base"),
    MovedModule("BaseHTTPServer", "BaseHTTPServer", "http.server"),
    MovedModule("CGIHTTPServer", "CGIHTTPServer", "http.server"),
    MovedModule("SimpleHTTPServer", "SimpleHTTPServer", "http.server"),
    MovedModule("cPickle", "cPickle", "pickle"),
    MovedModule("queue", "Queue"),
    MovedModule("reprlib", "repr"),
    MovedModule("socketserver", "SocketServer"),
    MovedModule("_thread", "thread", "_thread"),
    MovedModule("tkinter", "Tkinter"),
    MovedModule("tkinter_dialog", "Dialog", "tkinter.dialog"),
    MovedModule("tkinter_filedialog", "FileDialog", "tkinter.filedialog"),
    MovedModule("tkinter_scrolledtext", "ScrolledText", "tkinter.scrolledtext"),
    MovedModule("tkinter_simpledialog", "SimpleDialog", "tkinter.simpledialog"),
    MovedModule("tkinter_tix", "Tix", "tkinter.tix"),
    MovedModule("tkinter_ttk", "ttk", "tkinter.ttk"),
    MovedModule("tkinter_constants", "Tkconstants", "tkinter.constants"),
    MovedModule("tkinter_dnd", "Tkdnd", "tkinter.dnd"),
    MovedModule("tkinter_colorchooser", "tkColorChooser",
                "tkinter.colorchooser"),
    MovedModule("tkinter_commondialog", "tkCommonDialog",
                "tkinter.commondialog"),
    MovedModule("tkinter_tkfiledialog", "tkFileDialog", "tkinter.filedialog"),
    MovedModule("tkinter_font", "tkFont", "tkinter.font"),
    MovedModule("tkinter_messagebox", "tkMessageBox", "tkinter.messagebox"),
    MovedModule("tkinter_tksimpledialog", "tkSimpleDialog",
                "tkinter.simpledialog"),
    MovedModule("urllib_parse", __name__ + ".moves.urllib_parse", "urllib.parse"),
    MovedModule("urllib_error", __name__ + ".moves.urllib_error", "urllib.error"),
    MovedModule("urllib", __name__ + ".moves.urllib", __name__ + ".moves.urllib"),
    MovedModule("urllib_robotparser", "robotparser", "urllib.robotparser"),
    MovedModule("xmlrpc_client", "xmlrpclib", "xmlrpc.client"),
    MovedModule("winreg", "_winreg"),
]
for attr in _moved_attributes:
    setattr(_MovedItems, attr.name, attr)
    if isinstance(attr, MovedModule):
        sys.modules[__name__ + ".moves." + attr.name] = attr
del attr

_MovedItems._moved_attributes = _moved_attributes

moves = sys.modules[__name__ + ".moves"] = _MovedItems(__name__ + ".moves")


class Module_six_moves_urllib_parse(_LazyModule):
    """Lazy loading of moved objects in future.standard_library.moves.urllib_parse"""


_urllib_parse_moved_attributes = [
    MovedAttribute("ParseResult", "urlparse", "urllib.parse"),
    MovedAttribute("parse_qs", "urlparse", "urllib.parse"),
    MovedAttribute("parse_qsl", "urlparse", "urllib.parse"),
    MovedAttribute("urldefrag", "urlparse", "urllib.parse"),
    MovedAttribute("urljoin", "urlparse", "urllib.parse"),
    MovedAttribute("urlparse", "urlparse", "urllib.parse"),
    MovedAttribute("urlsplit", "urlparse", "urllib.parse"),
    MovedAttribute("urlunparse", "urlparse", "urllib.parse"),
    MovedAttribute("urlunsplit", "urlparse", "urllib.parse"),
    MovedAttribute("quote", "urllib", "urllib.parse"),
    MovedAttribute("quote_plus", "urllib", "urllib.parse"),
    MovedAttribute("unquote", "urllib", "urllib.parse"),
    MovedAttribute("unquote_plus", "urllib", "urllib.parse"),
    MovedAttribute("urlencode", "urllib", "urllib.parse"),
]
for attr in _urllib_parse_moved_attributes:
    setattr(Module_six_moves_urllib_parse, attr.name, attr)
del attr

Module_six_moves_urllib_parse._moved_attributes = _urllib_parse_moved_attributes

sys.modules[__name__ + ".moves.urllib_parse"] = sys.modules[__name__ + ".moves.urllib.parse"] = Module_six_moves_urllib_parse(__name__ + ".moves.urllib_parse")


class Module_six_moves_urllib_error(_LazyModule):
    """Lazy loading of moved objects in future.standard_library.moves.urllib_error"""


_urllib_error_moved_attributes = [
    MovedAttribute("URLError", "urllib2", "urllib.error"),
    MovedAttribute("HTTPError", "urllib2", "urllib.error"),
    MovedAttribute("ContentTooShortError", "urllib", "urllib.error"),
]
for attr in _urllib_error_moved_attributes:
    setattr(Module_six_moves_urllib_error, attr.name, attr)
del attr

Module_six_moves_urllib_error._moved_attributes = _urllib_error_moved_attributes

sys.modules[__name__ + ".moves.urllib_error"] = sys.modules[__name__ + ".moves.urllib.error"] = Module_six_moves_urllib_error(__name__ + ".moves.urllib.error")


class Module_six_moves_urllib_request(_LazyModule):
    """Lazy loading of moved objects in future.standard_library.moves.urllib_request"""


_urllib_request_moved_attributes = [
    MovedAttribute("urlopen", "urllib2", "urllib.request"),
    MovedAttribute("install_opener", "urllib2", "urllib.request"),
    MovedAttribute("build_opener", "urllib2", "urllib.request"),
    MovedAttribute("pathname2url", "urllib", "urllib.request"),
    MovedAttribute("url2pathname", "urllib", "urllib.request"),
    MovedAttribute("getproxies", "urllib", "urllib.request"),
    MovedAttribute("Request", "urllib2", "urllib.request"),
    MovedAttribute("OpenerDirector", "urllib2", "urllib.request"),
    MovedAttribute("HTTPDefaultErrorHandler", "urllib2", "urllib.request"),
    MovedAttribute("HTTPRedirectHandler", "urllib2", "urllib.request"),
    MovedAttribute("HTTPCookieProcessor", "urllib2", "urllib.request"),
    MovedAttribute("ProxyHandler", "urllib2", "urllib.request"),
    MovedAttribute("BaseHandler", "urllib2", "urllib.request"),
    MovedAttribute("HTTPPasswordMgr", "urllib2", "urllib.request"),
    MovedAttribute("HTTPPasswordMgrWithDefaultRealm", "urllib2", "urllib.request"),
    MovedAttribute("AbstractBasicAuthHandler", "urllib2", "urllib.request"),
    MovedAttribute("HTTPBasicAuthHandler", "urllib2", "urllib.request"),
    MovedAttribute("ProxyBasicAuthHandler", "urllib2", "urllib.request"),
    MovedAttribute("AbstractDigestAuthHandler", "urllib2", "urllib.request"),
    MovedAttribute("HTTPDigestAuthHandler", "urllib2", "urllib.request"),
    MovedAttribute("ProxyDigestAuthHandler", "urllib2", "urllib.request"),
    MovedAttribute("HTTPHandler", "urllib2", "urllib.request"),
    MovedAttribute("HTTPSHandler", "urllib2", "urllib.request"),
    MovedAttribute("FileHandler", "urllib2", "urllib.request"),
    MovedAttribute("FTPHandler", "urllib2", "urllib.request"),
    MovedAttribute("CacheFTPHandler", "urllib2", "urllib.request"),
    MovedAttribute("UnknownHandler", "urllib2", "urllib.request"),
    MovedAttribute("HTTPErrorProcessor", "urllib2", "urllib.request"),
    MovedAttribute("urlretrieve", "urllib", "urllib.request"),
    MovedAttribute("urlcleanup", "urllib", "urllib.request"),
    MovedAttribute("URLopener", "urllib", "urllib.request"),
    MovedAttribute("FancyURLopener", "urllib", "urllib.request"),
    MovedAttribute("proxy_bypass", "urllib", "urllib.request"),
]
for attr in _urllib_request_moved_attributes:
    setattr(Module_six_moves_urllib_request, attr.name, attr)
del attr

Module_six_moves_urllib_request._moved_attributes = _urllib_request_moved_attributes

sys.modules[__name__ + ".moves.urllib_request"] = sys.modules[__name__ + ".moves.urllib.request"] = Module_six_moves_urllib_request(__name__ + ".moves.urllib.request")


class Module_six_moves_urllib_response(_LazyModule):
    """Lazy loading of moved objects in future.standard_library.moves.urllib_response"""


_urllib_response_moved_attributes = [
    MovedAttribute("addbase", "urllib", "urllib.response"),
    MovedAttribute("addclosehook", "urllib", "urllib.response"),
    MovedAttribute("addinfo", "urllib", "urllib.response"),
    MovedAttribute("addinfourl", "urllib", "urllib.response"),
]
for attr in _urllib_response_moved_attributes:
    setattr(Module_six_moves_urllib_response, attr.name, attr)
del attr

Module_six_moves_urllib_response._moved_attributes = _urllib_response_moved_attributes

sys.modules[__name__ + ".moves.urllib_response"] = sys.modules[__name__ + ".moves.urllib.response"] = Module_six_moves_urllib_response(__name__ + ".moves.urllib.response")


class Module_six_moves_urllib_robotparser(_LazyModule):
    """Lazy loading of moved objects in future.standard_library.moves.urllib_robotparser"""


_urllib_robotparser_moved_attributes = [
    MovedAttribute("RobotFileParser", "robotparser", "urllib.robotparser"),
]
for attr in _urllib_robotparser_moved_attributes:
    setattr(Module_six_moves_urllib_robotparser, attr.name, attr)
del attr

Module_six_moves_urllib_robotparser._moved_attributes = _urllib_robotparser_moved_attributes

sys.modules[__name__ + ".moves.urllib_robotparser"] = sys.modules[__name__ + ".moves.urllib.robotparser"] = Module_six_moves_urllib_robotparser(__name__ + ".moves.urllib.robotparser")


class Module_six_moves_urllib(types.ModuleType):
    """Create a future.standard_library.moves.urllib namespace that resembles the Python 3 namespace"""
    parse = sys.modules[__name__ + ".moves.urllib_parse"]
    error = sys.modules[__name__ + ".moves.urllib_error"]
    request = sys.modules[__name__ + ".moves.urllib_request"]
    response = sys.modules[__name__ + ".moves.urllib_response"]
    robotparser = sys.modules[__name__ + ".moves.urllib_robotparser"]

    def __dir__(self):
        return ['parse', 'error', 'request', 'response', 'robotparser']


sys.modules[__name__ + ".moves.urllib"] = Module_six_moves_urllib(__name__ + ".moves.urllib")


def add_move(move):
    """Add an item to future.standard_library.moves."""
    setattr(_MovedItems, move.name, move)


def remove_move(name):
    """Remove item from future.standard_library.moves."""
    try:
        delattr(_MovedItems, name)
    except AttributeError:
        try:
            del moves.__dict__[name]
        except KeyError:
            raise AttributeError("no such move, %r" % (name,))
### End of code pasted from six.py v1.5.2 by Benjamin Peterson ###


# As of v0.12, this no longer happens by default:
# if not utils.PY3:
#     install_hooks()
