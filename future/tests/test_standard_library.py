"""
Tests for the future.standard_library module
"""

from __future__ import absolute_import, unicode_literals, print_function
from future import standard_library
from future import utils
from future.tests.base import unittest

import sys
import tempfile
import os

from future.standard_library import RENAMES, REPLACED_MODULES
from future.tests.base import CodeHandler


class TestStandardLibraryRenames(CodeHandler):

    def setUp(self):
        self.interpreter = 'python'
        self.tempdir = tempfile.mkdtemp() + os.path.sep

    @unittest.skipIf(utils.PY3, 'generic import tests are for Py2 only')
    def test_all(self):
        """
        Tests whether all of the old imports in RENAMES are accessible
        under their new names.
        """
        for (oldname, newname) in RENAMES.items():
            if newname == 'winreg' and sys.platform not in ['win32', 'win64']:
                continue
            if newname in REPLACED_MODULES:
                # Skip this check for e.g. the stdlib's ``test`` module,
                # which we have replaced completely.
                continue
            oldmod = __import__(oldname)
            newmod = __import__(newname)
            if '.' not in oldname:
                self.assertEqual(oldmod, newmod)

    def test_suspend_hooks(self):
        example_PY2_check = False
        with standard_library.suspend_hooks():
            # An example of fragile import code that we don't want to break:
            try:
                import builtins
            except ImportError:
                example_PY2_check = True
        if utils.PY2:
            self.assertTrue(example_PY2_check)
        else:
            self.assertFalse(example_PY2_check)
        # The import should succeed again now:
        import builtins

    def test_disable_hooks(self):
        example_PY2_check = False
        standard_library.disable_hooks()
        # An example of fragile import code that we don't want to break:
        try:
            import builtins
        except ImportError:
            example_PY2_check = True
        if utils.PY2:
            self.assertTrue(example_PY2_check)
        else:
            self.assertFalse(example_PY2_check)
        standard_library.enable_hooks()
        # The import should succeed again now:
        import builtins

    @unittest.skipIf(utils.PY3, 'not testing for old urllib on Py3')
    def test_old_urllib_import(self):
        """
        Tests whether an imported module can import the old urllib package.
        Importing future.standard_library in a script should be possible and
        not disrupt any uses of the old Py2 standard library names in modules
        imported by that script.
        """
        code1 = '''
                from future import standard_library
                import module_importing_old_urllib
                '''
        self._write_test_script(code1, 'runme.py')
        code2 = '''
                import urllib
                assert 'urlopen' in dir(urllib)
                print('Import succeeded!')
                '''
        self._write_test_script(code2, 'module_importing_old_urllib.py')
        output = self._run_test_script('runme.py')
        print(output)
        self.assertTrue(True)

    def test_sys_intern(self):
        """
        Py2's builtin intern() has been moved to the sys module. Tests
        whether sys.intern is available.
        """
        from sys import intern
        if utils.PY3:
            self.assertEqual(intern('hello'), 'hello')
        else:
            # intern() requires byte-strings on Py2:
            self.assertEqual(intern(b'hello'), b'hello')

    def test_sys_maxsize(self):
        """
        Tests whether sys.maxsize is available.
        """
        from sys import maxsize
        print(maxsize)
        self.assertTrue(maxsize > 0)

    def test_itertools_filterfalse(self):
        """
        Tests whether itertools.filterfalse is available.
        """
        from itertools import filterfalse
        not_div_by_3 = filterfalse(lambda x: x % 3 == 0, range(8))
        self.assertEqual(list(not_div_by_3), [1, 2, 4, 5, 7])

    def test_itertools_zip_longest(self):
        """
        Tests whether itertools.zip_longest is available.
        """
        from itertools import zip_longest
        a = (1, 2)
        b = [2, 4, 6]
        self.assertEqual(list(zip_longest(a, b)),
                         [(1, 2), (2, 4), (None, 6)])

    def test_import_from_module(self):
        """
        Tests whether e.g. "import socketserver" succeeds in a module
        imported by another module.
        """
        code1 = '''
                from future import standard_library
                import importme2
                '''
        code2 = '''
                import socketserver
                print('Import succeeded!')
                '''
        self._write_test_script(code1, 'importme1.py')
        self._write_test_script(code2, 'importme2.py')
        output = self._run_test_script('importme1.py')
        print(output)

    def test_configparser(self):
        import configparser
    
    def test_copyreg(self):
        import copyreg

    def test_pickle(self):
        import pickle

    def test_profile(self):
        import profile
    
    def test_stringio(self):
        from io import StringIO
        s = StringIO('test')
        for method in ['tell', 'read', 'seek', 'close', 'flush']:
            self.assertTrue(hasattr(s, method))

    def test_bytesio(self):
        from io import BytesIO
        s = BytesIO(b'test')
        for method in ['tell', 'read', 'seek', 'close', 'flush', 'getvalue']:
            self.assertTrue(hasattr(s, method))

    def test_queue(self):
        import queue
        q = queue.Queue()
        q.put('thing')
        self.assertFalse(q.empty())

    def test_reprlib(self):
        import reprlib

    def test_socketserver(self):
        import socketserver

    @unittest.skip("Not testing tkinter import (it may be installed separately from Python)")
    def test_tkinter(self):
        import tkinter

    def test_builtins(self):
        import builtins
        self.assertTrue(hasattr(builtins, 'tuple'))

    @unittest.skip("skipping in case there's no net connection")
    def test_urllib_request(self):
        import urllib.request
        from pprint import pprint
        URL = 'http://pypi.python.org/pypi/{0}/json'
        package = 'future'
        r = urllib.request.urlopen(URL.format(package))
        # pprint(r.read().decode('utf-8'))

    def test_html_import(self):
        import html
        import html.entities
        import html.parser

    def test_http_client_import(self):
        import http.client
        self.assertTrue(True)

    @unittest.expectedFailure
    def test_http_imports(self):
        import http
        import http.server
        import http.cookies
        import http.cookiejar

    @unittest.expectedFailure
    def test_urllib_imports(self):
        import urllib
        import urllib.parse
        import urllib.request
        import urllib.robotparser
        import urllib.error
        import urllib.response
        self.assertTrue(True)

    @unittest.expectedFailure
    def test_urllib_parse(self):
        import urllib.parse
        URL = 'http://pypi.python.org/test_url/spaces oh no/'
        self.assertEqual(urllib.parse.quote(URL.format(package)), 'http%3A//pypi.python.org/test_url/spaces%20oh%20no/')

    def test_underscore_prefixed_modules(self):
        import _thread
        import _dummy_thread
        import _markupbase
        self.assertTrue(True)

    def test_reduce(self):
        """
        reduce has been moved to the functools module
        """
        import functools
        self.assertEqual(functools.reduce(lambda x, y: x+y, range(1, 6)), 15)

    def test_collections_userstuff(self):
        """
        UserDict, UserList, and UserString have been moved to the
        collections module.
        """
        from collections import UserDict
        from collections import UserList
        from collections import UserString

    def test_reload(self):
        """
        reload has been moved to the imp module
        """
        import imp
        imp.reload(imp)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
