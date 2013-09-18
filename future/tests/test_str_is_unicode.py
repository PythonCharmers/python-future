# -*- coding: utf-8 -*-
"""
Tests for the future.str_is_unicode module
"""

from __future__ import absolute_import, unicode_literals, print_function
from future.builtins import *
from future import utils

import unittest

TEST_UNICODE_STR = u'ℝεα∂@ßʟ℮ ☂ℯṧт υηḯ¢☺ḓ℮'


class TestStrIsUnicode(unittest.TestCase):
    def test_str(self):
        self.assertIsNot(str, bytes)            # Py2: assertIsNot only in 2.7
        self.assertEqual(str('blah'), u'blah')  # u'' prefix: Py3.3 and Py2 only

    def test_str_encode_decode(self):
        a = u'Unicode string: \u5b54\u5b50'
        self.assertEqual(str(a), a.encode('utf-8').decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
