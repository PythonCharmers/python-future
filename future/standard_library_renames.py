"""
Python 3 reorganized the standard library (PEP 3108). This module exposes
several standard library modules to Python 2 under their new Python 3 names.

It is designed to be used as follows:

    from future import standard_library_renames

And then, for example:

    import builtins
    import configparser
    import copyreg
    import queue
    import socketserver
    import tkinter

We don't currently support these, but would like to:

    import http.cookies
    import http.server
    import urllib.parse
    import xmlrpc.client

This module only supports Python 2.7 and Python 3.1+.
"""

from __future__ import absolute_import, print_function

import inspect
import importlib
import sys
import warnings

from . import six

# mapping = {'ConfigParser': 'configparser',
#            'Queue': 'queue',
#            'SocketServer': 'socketserver',
#            'Tkinter': 'tkinter',
#            '__builtin__': 'builtins',
#            'copy_reg': 'copyreg'}

mapping = {thing.mod: thing.name for thing in six._moved_attributes \
           if isinstance(thing, six.MovedModule)}



# class ImportBlocker(object):
#     def __init__(self, *args):
#         self.module_names = args
#     
#     def find_module(self, fullname, path=None):
#         if fullname in self.module_names:
#             return self
#         return None
#     
#     def load_module(self, name):
#         raise ImportError("%s is blocked and cannot be imported" % name)
# 
# print(sys.meta_path)
# sys.meta_path = [ImportBlocker('ConfigParser')]

	

import logging
import imp
import sys
 
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
 
sys.meta_path = [WarnOnImport('getopt', 'optparse', # etc.
                                 )]



if not six.PY3:
    for oldname, newname in mapping.items():
        # print('Importing module ' + oldname)
        try:
            module = importlib.import_module(oldname, package=None)
        except ImportError as e:
            # Expected to fail:
            if not oldname == '_winreg':
                warnings.warn('Could not import module ' + oldname)
        else:
            sys.modules[newname] = module
        sys.modules[oldname] = None
        # module.__name__ = newname   # has no effect?!

    caller = inspect.currentframe().f_back
    # caller.f_globals[newname] = oldname

print(len(sys.modules))
