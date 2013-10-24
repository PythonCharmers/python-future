# -*- coding: utf-8 -*-
"""
Tests for the various utility functions and classes in ``future.utils``
"""

from __future__ import absolute_import, unicode_literals, print_function
from future.builtins import *
from future import utils

import unittest

TEST_UNICODE_STR = u'ℝεα∂@ßʟ℮ ☂ℯṧт υηḯ¢☺ḓ℮'


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.s = TEST_UNICODE_STR
        self.s2 = str(self.s)
        self.b = b'ABCDEFG'
        self.b2 = bytes(self.b)

    def test_native(self):   
        a = int(10**20)     # long int
        b = utils.native(a)
        if utils.PY2:
            self.assertEqual(type(b), long)
        else:
            self.assertEqual(type(b), int))
    
        c = bytes(b'ABC')
        d = native(c)
        if utils.PY2:
            self.assertEqual(type(d), type(b'Py2 byte-string')
        else:
            self.assertEqual(type(d), bytes))
    
        s = str(u'ABC')
        t = native(s)
        if utils.PY2:
            self.assertEqual(type(t), unicode)
        else:
            self.assertEqual(type(t), str)
        type(s)

    def test_istext(self):
        self.assertTrue(utils.istext(self.s))
        self.assertTrue(utils.istext(self.s2))
        self.assertFalse(utils.istext(self.b))
        self.assertFalse(utils.istext(self.b2))

    def test_isbytes(self):
        self.assertTrue(utils.isbytes(self.b))
        self.assertTrue(utils.isbytes(self.b2))
        self.assertFalse(utils.isbytes(self.s))
        self.assertFalse(utils.isbytes(self.s2))


if __name__ == '__main__':
    unittest.main()
