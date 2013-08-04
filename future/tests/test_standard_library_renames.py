"""
Tests for the future.standard_library module
"""

from __future__ import absolute_import, unicode_literals, print_function
from future import standard_library
from future import six

import sys
import textwrap
import unittest
from subprocess import check_output

from future.standard_library import RENAMES, REPLACED_MODULES


class TestStandardLibraryRenames(unittest.TestCase):

    def setUp(self):
        self.interpreter = 'python'

    @unittest.skipIf(six.PY3, 'generic import tests are for Py2 only')
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

    def test_import_from_module(self):
        """
        Tests whether e.g. "import socketserver" succeeds in a module imported by another module.
        """
        code1 = '''
                from future import standard_library
                import importme2
                '''
        code2 = '''
                import socketserver
                print('Import succeeded!')
                '''
        with open('importme1.py', 'w') as f:
            f.write(textwrap.dedent(code1))
        with open('importme2.py', 'w') as f:
            f.write(textwrap.dedent(code2))
        output = check_output([self.interpreter, 'importme1.py'])
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

    # @unittest.skip("skipping in case there's no net connection")
    @unittest.expectedFailure
    def test_urllib_request(self):
        import urllib.request
        from pprint import pprint
        URL = 'http://pypi.python.org/pypi/{}/json'
        package = 'future'
        r = urllib.request.urlopen(URL.format(package))
        pprint(r.read().decode('utf-8'))

    def test_html_import(self):
        import html
        import html.entities
        import html.parser
        self.assertTrue(True)

    @unittest.expectedFailure
    def test_http_import(self):
        import http
        import http.server
        import http.client
        import http.cookies
        import http.cookiejar
        self.assertTrue(True)

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

    @unittest.expectedFailure     # currently fails on Py2
    def test_sys_intern(self):
        """
        intern() has been moved to the sys module.
        """
        from future import standard_library
        from sys import intern
        intern('mystring')
        self.assertTrue(True)

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

    def test_reload(self):
        """
        reload has been moved to the imp module
        """
        import imp
        imp.reload(imp)
        self.assertTrue(True)

        
if __name__ == '__main__':
    unittest.main()
