"""
Python 3 reorganized the standard library (PEP 3108). This module exposes
several standard library modules to Python 2 under their new Python 3
names.

It is designed to be used as follows:

    from future import standard_library_renames

And then these imports work:

    import builtins
    import configparser
    import copyreg
    import io
    import _markupbase
    import queue
    import reprlib
    import socketserver
    import tkinter
    import winreg (on Windows only)

The modules are still available under their old names on Python 2.

We don't currently support these, but would like to:

    import pickle (should bring in cPickle on Python 2)
    import http.cookies
    import http.cookiejar
    import http.server
    import http.client
    import dbm
    import dbm.dumb
    import dbm.gnu
    import urllib.request
    import urllib.parse
    import urllib.error
    import xmlrpc.client
    import urllib.robotparser
    import test.support
    import xmlrpc.client

This module only supports Python 2.7 and Python 3.1+.
"""

from __future__ import absolute_import, print_function

import sys
import logging
import imp

from . import six


# A subset of six.moves:
RENAMES = {
           # 'anydbm': 'dbm',   # causes infinite import loop 
           # 'whichdb': 'dbm',  # causes infinite import loop 
           'ConfigParser': 'configparser',
           'copy_reg': 'copyreg',
           'cPickle': 'pickle',
           # 'cProfile': 'profile',: included in Python 3.3
           'cStringIO': 'io',
           'markupbase': '_markupbase',
           'Queue': 'queue',
           'repr': 'reprlib',
           'SocketServer': 'socketserver',
           'Tkinter': 'tkinter',
           '_winreg': 'winreg',
           '__builtin__': 'builtins',
          }


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
    def __init__(self, old_to_new):
        '''
        Pass in a dictionary-like object mapping from old names to new
        names. E.g. {'ConfigParser': 'configparser', 'cPickle': 'pickle'}
        '''
        self.old_to_new = old_to_new
        both = set(old_to_new.keys()) & set(old_to_new.values())
        # print(both)
        assert len(both) == 0, 'Ambiguity in renaming (handler not implemented'
        self.new_to_old = {new: old for (old, new) in old_to_new.items()}
 
    def find_module(self, fullname, path=None):
        if fullname in set(self.old_to_new) | set(self.new_to_old):
            self.path = path
            return self
        return None
 
    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]
        if name in self.new_to_old:
            # New name
            oldname = self.new_to_old[name]
            module_info = imp.find_module(oldname, self.path)
            module = imp.load_module(oldname, *module_info)
        elif name in self.old_to_new:
            # Old name. Import with warning.
            module_info = imp.find_module(name, self.path)
            module = imp.load_module(name, *module_info)
            logging.warning("Imported deprecated module %s", name)
        else: 
            # Something else
            module_info = imp.find_module(name, self.path)
            module = imp.load_module(name, *module_info)
        sys.modules[name] = module
        return module
 

if not six.PY3:
    sys.meta_path = [RenameImport(RENAMES)]

