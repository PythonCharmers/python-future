# -*- coding: utf-8 -*-
"""
Tests for the surrogateescape codec
"""

from __future__ import absolute_import, division, unicode_literals
from future.builtins import (bytes, dict, int, range, round, str, super,
                             ascii, chr, hex, input, next, oct, open, pow,
                             filter, map, zip)
from future.utils.surrogateescape import register_surrogateescape
from future.tests.base import unittest


class TestSurrogateEscape(unittest.TestCase):
    def setUp(self):
        register_surrogateescape()

    def test_surrogateescape(self):
        s = b'From: foo@bar.com\nTo: baz\nMime-Version: 1.0\nContent-Type: text/plain; charset=utf-8\nContent-Transfer-Encoding: base64\n\ncMO2c3RhbA\xc3\xa1=\n'
        u = 'From: foo@bar.com\nTo: baz\nMime-Version: 1.0\nContent-Type: text/plain; charset=utf-8\nContent-Transfer-Encoding: base64\n\ncMO2c3RhbA\udcc3\udca1=\n'
        s2 = s.decode('ASCII', errors='surrogateescape')
        self.assertEqual(s2, u)


if __name__ == '__main__':
    unittest.main()
