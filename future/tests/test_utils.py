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

    def test_is_text(self):
        self.assertTrue(utils.is_text(self.s))
        self.assertTrue(utils.is_text(self.s2))
        self.assertFalse(utils.is_text(self.b))
        self.assertFalse(utils.is_text(self.b2))

    def test_is_bytes(self):
        self.assertTrue(utils.is_bytes(self.b))
        self.assertTrue(utils.is_bytes(self.b2))
        self.assertFalse(utils.is_bytes(self.s))
        self.assertFalse(utils.is_bytes(self.s2))


if __name__ == '__main__':
    unittest.main()
