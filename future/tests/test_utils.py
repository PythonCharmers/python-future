# -*- coding: utf-8 -*-
"""
Tests for the various utility functions and classes in ``future.utils``
"""

from __future__ import absolute_import, unicode_literals, print_function
import sys
from future.builtins import *
from future.utils import (old_div, istext, isbytes, native, PY2, PY3,
                         native_str, raise_, as_native_str, ensure_new_type,
                         bytes_to_native_str)

from numbers import Integral
from future.tests.base import unittest, skip26


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

        d1 = dict({'a': 1, 'b': 2})
        d2 = native(d1)
        self.assertEqual(d1, d2)
        self.assertEqual(type(d2), type({}))

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

    @skip26
    def test_raise_(self):
        """
        The with_value() test currently fails on Py3
        """
        def valerror():
            try:
                raise ValueError("Apples!")
            except Exception as e:
                raise_(e)

        self.assertRaises(ValueError, valerror)

        def with_value():
            raise_(IOError, "This is an error")

        self.assertRaises(IOError, with_value)

        try:
            with_value()
        except IOError as e:
            self.assertEqual(str(e), "This is an error")

        def with_traceback():
            try:
                raise ValueError("An error")
            except Exception as e:
                _, _, traceback = sys.exc_info()
                raise_(IOError, str(e), traceback)

        self.assertRaises(IOError, with_traceback)

        try:
            with_traceback()
        except IOError as e:
            self.assertEqual(str(e), "An error")


    def test_as_native_str(self):
        """
        Tests the decorator as_native_str()
        """
        class MyClass(object):
            @as_native_str()
            def __repr__(self):
                return u'abc'
            
        obj = MyClass()
       
        self.assertEqual(repr(obj), 'abc')
        if PY2:
            self.assertEqual(repr(obj), b'abc')
        else:
            self.assertEqual(repr(obj), u'abc')

    def test_ensure_new_type(self):
        s = u'abcd'
        s2 = str(s)
        self.assertEqual(ensure_new_type(s), s2)
        self.assertEqual(type(ensure_new_type(s)), str)

        b = b'xyz'
        b2 = bytes(b)
        self.assertEqual(ensure_new_type(b), b2)
        self.assertEqual(type(ensure_new_type(b)), bytes)

        i = 10000000000000
        i2 = int(i)
        self.assertEqual(ensure_new_type(i), i2)
        self.assertEqual(type(ensure_new_type(i)), int)

    def test_bytes_to_native_str(self):
        """
        Test for issue #47
        """
        b = bytes(b'abc')
        s = bytes_to_native_str(b)
        if PY2:
            self.assertEqual(s, b)
        else:
            self.assertEqual(s, 'abc')
        self.assertTrue(isinstance(s, native_str))
        self.assertEqual(type(s), native_str)


if __name__ == '__main__':
    unittest.main()
