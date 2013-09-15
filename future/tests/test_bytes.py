# -*- coding: utf-8 -*-
"""
Tests for the hacks to the bytes object
"""

from __future__ import absolute_import, unicode_literals, print_function
from future.builtins import *
from future.builtins.backports import cursedbytes
from future import utils

from future.builtins.backports import hopefullynothackedbytes

import unittest

TEST_UNICODE_STR = u'ℝεα∂@ßʟ℮ ☂ℯṧт υηḯ¢☺ḓ℮'
# Tk icon as a .gif:
TEST_BYTE_STR = b'GIF89a\x0e\x00\x0b\x00\x80\xff\x00\xff\x00\x00\xc0\xc0\xc0!\xf9\x04\x01\x00\x00\x01\x00,\x00\x00\x00\x00\x0e\x00\x0b\x00@\x02\x1f\x0c\x8e\x10\xbb\xcan\x90\x99\xaf&\xd8\x1a\xce\x9ar\x06F\xd7\xf1\x90\xa1c\x9e\xe8\x84\x99\x89\x97\xa2J\x01\x00;\x1a\x14\x00;;\xba\nD\x14\x00\x00;;'


class TestStrIsUnicode(unittest.TestCase):
    @unittest.expectedFailure  # on Python 2
    def test_bytes_encoding_arg(self):
        """
        The bytes class has changed in Python 3 to accept an
        additional argument in the constructor: encoding.

        It would be nice to support this without breaking the
        isinstance(..., bytes) test below.
        """
        u = u'Unicode string: \u5b54\u5b50'
        b = bytes(u, encoding='utf-8')
        self.assertEqual(b, u.encode('utf-8'))

    def test_bytes_fromhex(self):
        self.assertEqual(bytes.fromhex('bb 0f'), b'\xbb\x0f')
        b = b'My bytestring'
        self.assertEqual(b.fromhex('bb 0f'), b'\xbb\x0f')

    def test_isinstance_bytes(self):
        self.assertEqual(isinstance(b'blah', bytes), True)
        # The next test ensures the bytes object hasn't been shadowed by
        # something that breaks any isinstance checks like this in user code:
        self.assertEqual(isinstance(u'blah'.encode('utf-8'), bytes), True)


if __name__ == '__main__':
    unittest.main()
