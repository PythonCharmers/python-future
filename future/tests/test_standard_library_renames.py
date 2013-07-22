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
    
    def test_io(self):
        from io import StringIO
        s = StringIO('test')
        for method in ['next', 'read', 'seek', 'close']:
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

    @unittest.skip("Test only works if the python-tk package is installed")
    def test_tkinter(self):
        import tkinter


    # '_winreg': 'winreg',

    def test_builtins(self):
        import builtins
        self.assertTrue(hasattr(builtins, 'tuple'))


if __name__ == '__main__':
    unittest.main()
