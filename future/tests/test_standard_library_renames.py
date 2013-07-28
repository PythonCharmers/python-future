"""
Tests for the future.standard_library_renames module
"""

from __future__ import absolute_import, unicode_literals, print_function
from future import standard_library_renames, six

import unittest


class TestStandardLibraryRenames(unittest.TestCase):
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

    # 'markupbase': '_markupbase',

    def test_reprlib(self):
        import reprlib

    def test_socketserver(self):
        import socketserver

    @unittest.skip("Not testing tkinter import (it may be installed separately from Python)")
    def test_tkinter(self):
        import tkinter


    # '_winreg': 'winreg',

    def test_builtins(self):
        import builtins
        self.assertTrue(hasattr(builtins, 'tuple'))

    @unittest.skip("skipping in case there's no net connection")
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

    def test_http_import(self):
        import http
        import http.server
        import http.client
        import http.cookies
        import http.cookiejar

    def test_urllib_imports(self):
        import urllib
        import urllib.parse
        import urllib.request
        import urllib.robotparser
        import urllib.error
        import urllib.response

    @unittest.expectedFailure
    def test_urllib_parse(self):
        import urllib.parse
        URL = 'http://pypi.python.org/test_url/spaces oh no/'
        assertEqual(urllib.parse.quote(URL.format(package)), 'http%3A//pypi.python.org/test_url/spaces%20oh%20no/')

    @unittest.expectedFailure     # currently fails on Py2
    def test_sys_intern(self):
        """
        intern() has been moved to the sys module.
        """
        from future import standard_library_renames
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
