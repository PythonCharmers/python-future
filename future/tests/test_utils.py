# -*- coding: utf-8 -*-
"""
Tests for the various utility functions and classes in ``future.utils``
"""

from __future__ import absolute_import, unicode_literals, print_function
from future.builtins import *
from future.utils import old_div, istext, isbytes, native, PY2, PY3, native_str

from numbers import Integral
from future.tests.base import unittest

TEST_UNICODE_STR = u'ℝεα∂@ßʟ℮ ☂ℯṧт υηḯ¢☺ḓ℮'


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.s = TEST_UNICODE_STR
        self.s2 = str(self.s)
        self.b = b'ABCDEFG'
        self.b2 = bytes(self.b)

    def test_old_div(self):
        """
        Tests whether old_div(a, b) is always equal to Python 2's a / b.
        """
        self.assertEqual(old_div(1, 2), 0)
        self.assertEqual(old_div(2, 2), 1)
        self.assertTrue(isinstance(old_div(2, 2), int))

        self.assertEqual(old_div(3, 2), 1)
        self.assertTrue(isinstance(old_div(3, 2), int))

        self.assertEqual(old_div(3., 2), 1.5)
        self.assertTrue(not isinstance(old_div(3., 2), int))

        self.assertEqual(old_div(-1, 2.), -0.5)
        self.assertTrue(not isinstance(old_div(-1, 2.), int))

        with self.assertRaises(ZeroDivisionError):
            old_div(0, 0)
        with self.assertRaises(ZeroDivisionError):
            old_div(1, 0)

    def test_native_str(self):
        """
        Tests whether native_str is really equal to the platform str.
        """
        if PY2:
            import __builtin__
            builtin_str = __builtin__.str
        else:
            import builtins
            builtin_str = builtins.str

        inputs = [b'blah', u'blah', 'blah']
        for s in inputs:
            self.assertEqual(native_str(s), builtin_str(s))
            self.assertTrue(isinstance(native_str(s), builtin_str))
        
    def test_native(self):   
        a = int(10**20)     # long int
        b = native(a)
        self.assertEqual(a, b)
        if PY2:
            self.assertEqual(type(b), long)
        else:
            self.assertEqual(type(b), int)
    
        c = bytes(b'ABC')
        d = native(c)
        self.assertEqual(c, d)
        if PY2:
            self.assertEqual(type(d), type(b'Py2 byte-string'))
        else:
            self.assertEqual(type(d), bytes)
    
        s = str(u'ABC')
        t = native(s)
        self.assertEqual(s, t)
        if PY2:
            self.assertEqual(type(t), unicode)
        else:
            self.assertEqual(type(t), str)
        type(s)

    def test_istext(self):
        self.assertTrue(istext(self.s))
        self.assertTrue(istext(self.s2))
        self.assertFalse(istext(self.b))
        self.assertFalse(istext(self.b2))

    def test_isbytes(self):
        self.assertTrue(isbytes(self.b))
        self.assertTrue(isbytes(self.b2))
        self.assertFalse(isbytes(self.s))
        self.assertFalse(isbytes(self.s2))


if __name__ == '__main__':
    unittest.main()
