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


REPLACED_MODULES = set(['test', 'urllib', 'pickle', 'email'])  # add dbm when we support it
# These are entirely new in Python 3.x, so they cause no potential clashes
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
            oldname = self.new_to_old[name]
            module = self._find_and_load_module(oldname)
        else:
            module = self._find_and_load_module(name)
        # In any case, make it available under the requested (Py3) name
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
        install_hooks()
        return self

    def __exit__(self, *args):
        logging.debug('Exiting hooks context manager')
        if not self.hooks_were_installed:
            # Reset sys.modules to how it was at the start.
            # sys.modules = self.old_sys_modules
            remove_hooks()


def is_py2_stdlib_module(m):
    """
    Tries to infer whether the module m is from the Python 2 standard library.
    This may not be reliable on all systems.
    """
    if utils.PY3:
        return False
    if not 'stdlib_path' in is_py2_stdlib_module.__dict__:
        stdlib_files = [contextlib.__file__, os.__file__, copy.__file__]
        stdlib_paths = [os.path.split(f)[0] for f in stdlib_files]
        if not len(set(stdlib_paths)) == 1:
            # This seems to happen on travis-ci.org. Very strange. We'll try to
            # ignore it.
            logging.warn('Multiple locations found for the Python standard '
                         'library: %s' % stdlib_paths)
        # Choose the first one arbitrarily
        is_py2_stdlib_module.stdlib_path = stdlib_paths[0]

    if m.__name__ in sys.builtin_module_names:
        return True

    if hasattr(m, '__file__'):
        modpath = os.path.split(m.__file__)
        if (modpath[0].startswith(is_py2_stdlib_module.stdlib_path) and
            'site-packages' not in modpath[0]):
            return True
        
    return False


def scrub_py2_sys_modules():
    """
    Removes any Python 2 standard library modules from ``sys.modules`` that
    would interfere with Py3-style imports using ``future.standard_library``
    import hooks.
    """
    if utils.PY3:
        return
    for modulename in REPLACED_MODULES:
        if not modulename in sys.modules:
            continue

        module = sys.modules[modulename]

        if is_py2_stdlib_module(module):
            logging.debug('Deleting {0} from sys.modules'.format(modulename))
            del sys.modules[modulename]


def scrub_future_sys_modules():
    """
    Removes modules from the ``sys.modules`` cache that would confuse code such
    as this:

        try:
            import builtins
        except:
            import __builtin__ as builtins

    or this:

        import urllib       # We want this to pull in only the Py2 module
                            # after scrub_future_sys_modules() has been called

    This includes items like this:
        key: new_py3_module_name
        value: either future.standard_library module or py2 module with
               another name
    """
    if utils.PY3:
        return
    for modulename, module in sys.modules.items():
        if modulename.startswith('future'):
            logging.debug('Not removing future module')

        # We don't want to remove Python 2.x urllib if this is cached.
        # But we do want to remove modules under their new names, e.g.
        # 'builtins'.
        # This code is probably broken:
        # if (is_py2_stdlib_module(module) and 
        #     not modulename in RENAMES.values()):
        #     continue

        # We look for builtins, configparser, urllib, email, http, etc., and
        # their submodules
        if (modulename in RENAMES.values() or 
            any(modulename.startswith(m + '.') for m in RENAMES.values())):   

            if module is None:
                # This happens for e.g. __future__ imports. Delete it.
                logging.debug('Deleting empty module {0} from sys.modules'
                              .format(modulename))
                del sys.modules[modulename]
                continue

            logging.warn('Deleting (future) {0} from sys.modules'
                         .format(modulename))
            del sys.modules[modulename]

            # Delete it whether or not the name clashes with a Py2 module name
            # if modulename not in REPLACED_MODULES:
            #     logging.debug('Deleting (future) {0} from sys.modules'.format(modulename))
            #     del sys.modules[modulename]
            #     continue

            # import pdb
            # pdb.set_trace()

            # # If it does clash with a Py2 module name (e.g. test or urllib),
            # # delete it anyway, because it would prevent normal imports from
            # # working.

            # if modulename in REPLACED_MODULES:
            #     logging.debug('Deleting (future) {0} from sys.modules'.format(modulename))
            #     del sys.modules[modulename]
            #     continue

            # # builtins has no __file__:
            # if not hasattr(module, '__file__'):
            #     pass

            # if hasattr(module, '__file__'):
            #     if not os.path.join('future', 'standard_library') in module.__file__:
            #         import pdb; pdb.set_trace()
            #         # Why would this occur?
            #         s = ('Please report this unknown condition as an issue on '
            #              'https://github.com/PythonCharmers/python-future: '
            #              '{0}, {1}').format(modulename, module.__file__)
            #         logging.warn(s)
            #         continue


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
        return self
    def __exit__(self, *args):
        if self.hooks_were_installed:
            install_hooks()
            # TODO: add any previously scrubbed modules back to the sys.modules
            # cache?


def install_hooks(keep_sys_modules=False):
    """
    This function installs the future.standard_library import hook into
    sys.meta_path. By default it also removes any Python 2 standard library
    modules from the ``sys.modules`` cache that would interfere the Py3-style
    ``future`` imports using the import hooks.

    To leave ``sys.modules`` cache alone, pass keep_sys_modules=True.
    """
    if utils.PY3:
        return
    if not keep_sys_modules:
        scrub_py2_sys_modules()    # in case they interfere ... e.g. urllib
    logging.debug('sys.meta_path was: {0}'.format(sys.meta_path))
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
    logging.debug('sys.meta_path is now: {0}'.format(sys.meta_path))


def enable_hooks():
    """
    Deprecated. Use install_hooks() instead. This will be removed by
    ``future`` v1.0.
    """
    install_hooks()


def remove_hooks(keep_sys_modules=False):
    """
    This function removes the import hook from sys.meta_path. By default it also removes
    any submodules of ``future.standard_library`` from the ``sys.modules``
    cache.

    To leave the ``sys.modules`` cache alone, pass keep_sys_modules=True.
    """
    if utils.PY3:
        return
    logging.debug('Uninstalling hooks ...')
    # Loop backwards, so deleting items keeps the ordering:
    for i, hook in list(enumerate(sys.meta_path))[::-1]:
        if hasattr(hook, 'RENAMER'):
            del sys.meta_path[i]
    if not keep_sys_modules:
        scrub_future_sys_modules()


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


# As of v0.12, this no longer happens by default:
if not utils.PY3:
    install_hooks()
