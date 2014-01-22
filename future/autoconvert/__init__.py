# -*- coding: utf-8 -*-
"""
future.autoconvert
==================

The ``future.autoconvert`` package provides an import hook for Python 3 which
runs ``futurize`` fixers over Python 2 code on import to convert print statements into
functions, etc.

It is intended to assist users when porting Python 2.x code to 3.x.

Usage
-----

Once installed on the path, the import hook is invoked as follows:

    >>> from future import autoconvert
    >>> autoconvert.install_hooks()

You can unregister the hook by

    >>> autoconvert.remove_hooks()


Inspired by ``uprefix`` by Vinay M. Sajip.
"""

import imp
from lib2to3.pgen2.parse import ParseError
from lib2to3.refactor import RefactoringTool
import logging
import marshal
import os
import sys
import pdb

from libfuturize import fixes2

__version__ = '0.1.0'

logger = logging.getLogger(__name__)

myfixes = (list(fixes2.libfuturize_2fix_names_stage1) +
           list(fixes2.lib2to3_fix_names_stage1) +
           list(fixes2.libfuturize_2fix_names_stage2) +
           list(fixes2.lib2to3_fix_names_stage2))

# There are two possible grammars: with or without the print statement.
# Hence we have two possible refactoring tool implementations.
# _rt = RefactoringTool(['libfuturize.fixes2.fix_print_with_import'])
_rt = RefactoringTool(myfixes)
_rtp = RefactoringTool(myfixes, {'print_function': True})

#
# We need to find a prefix for the standard library, as we don't want to
# process any files there (they will already be Python 3, and so won't have
# u prefixes anyway.
#
# In a non-pythonv virtualenv, sys.real_prefix points to the installed Python.
# In a pythonv venv, sys.base_prefix points to the installed Python.
# Outside a virtual environment, sys.prefix points to the installed Python.
#

# if hasattr(sys, 'real_prefix'):
#     _syslibprefix = sys.real_prefix
# else:
#     _syslibprefix = getattr(sys, 'base_prefix', sys.prefix)

class Py2Fixer(object):
    def __init__(self):
        self.found = None

    def find_module(self, fullname, path=None):
        # print('Running find_module ...')
        if '.' in fullname:
            parent, child = fullname.rsplit('.', 1)
            if path is None:
                loader = self.find_module(parent, path)
                mod = loader.load_module(parent)
                path = mod.__path__
            fullname = child

        self.found = imp.find_module(fullname, path)
        self.kind = self.found[-1][-1]
        if self.kind == imp.PKG_DIRECTORY:
            self.pathname = os.path.join(self.found[1], '__init__.py')
        elif self.kind == imp.PY_SOURCE:
            self.pathname = self.found[1]
        return self

    def transform(self, source):
        # pdb.set_trace()
        # print('Running transform() ...')
        # This implementation uses lib2to3,
        # you can override and use something else
        # if that's better for you

        # lib2to3 likes a newline at the end
        source += '\n'
        try:
            tree = _rt.refactor_string(source, self.pathname)
        except ParseError as e:
            if e.msg != 'bad input' or e.value != '=':
                raise
            tree = _rtp.refactor_string(source, self.pathname)
        # could optimise a bit for only doing str(tree) if
        # getattr(tree, 'was_changed', False) returns True
        return str(tree)[:-1] # remove added newline

    def load_module(self, fullname):
        # print('Running load_module ...')
        if fullname in sys.modules:
            mod = sys.modules[fullname]
        else:
            if self.kind in (imp.PY_COMPILED, imp.C_EXTENSION, imp.C_BUILTIN,
                             imp.PY_FROZEN):
                convert = False
            # elif self.pathname.startswith(_syslibprefix):
            #     convert = False
            # in theory, other paths could be configured to be excluded here, too
            else:
                convert = True
            if not convert:
                mod = imp.load_module(fullname, *self.found)
            else:
                mod = imp.new_module(fullname)
                sys.modules[fullname] = mod

                # required by PEP 302
                mod.__file__ = self.pathname
                mod.__name__ = fullname
                mod.__loader__ = self
                mod.__package__ = '.'.join(fullname.split('.')[:-1])
                
                if self.kind == imp.PKG_DIRECTORY:
                    mod.__path__ = [ os.path.dirname(self.pathname) ]
                #else, regular module
                try:
                    cachename = imp.cache_from_source(self.pathname)
                    if not os.path.exists(cachename):
                        update_cache = True
                    else:
                        sourcetime = os.stat(self.pathname).st_mtime
                        cachetime = os.stat(cachename).st_mtime
                        update_cache = cachetime < sourcetime
                    if not update_cache:
                        with open(cachename, 'rb') as f:
                            data = f.read()
                            try:
                                code = marshal.loads(data)
                            except Exception:
                                # pyc could be corrupt. Regenerate it
                                update_cache = True
                    if update_cache:
                        if self.found[0]:
                            source = self.found[0].read()
                        elif self.kind == imp.PKG_DIRECTORY:
                            with open(self.pathname) as f:
                                source = f.read()

                        source = self.transform(source)

                        code = compile(source, self.pathname, 'exec')
                        dirname = os.path.dirname(cachename)
                        if not os.path.exists(dirname):
                            os.makedirs(dirname)
                        try:
                            with open(cachename, 'wb') as f:
                                data = marshal.dumps(code)
                                f.write(data)
                        except Exception:   # could be write-protected
                            pass
                    exec(code, mod.__dict__)
                except Exception as e:
                    # must remove module from sys.modules
                    del sys.modules[fullname]
                    raise # keep it simple

        if self.found[0]:
            self.found[0].close()
        return mod

_hook = Py2Fixer()

def install_hooks():
    # pdb.set_trace()
    enable = sys.version_info[0] >= 3   # enabled for all 3.x
    # enable = (3, 0) <= sys.version_info[:2]            # enabled for 3.0+
    if enable and _hook not in sys.meta_path:   # was: if enable and _hook not in ...
        sys.meta_path.insert(0, _hook)
    # could return the hook when there are ways of configuring it
    #return _hook

def remove_hooks():
    # pdb.set_trace()
    if _hook in sys.meta_path:
        sys.meta_path.remove(_hook)

