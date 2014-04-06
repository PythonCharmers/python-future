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
        """
        From the backport of the email package
        """
        s = b'From: foo@bar.com\nTo: baz\nMime-Version: 1.0\nContent-Type: text/plain; charset=utf-8\nContent-Transfer-Encoding: base64\n\ncMO2c3RhbA\xc3\xa1=\n'
        u = 'From: foo@bar.com\nTo: baz\nMime-Version: 1.0\nContent-Type: text/plain; charset=utf-8\nContent-Transfer-Encoding: base64\n\ncMO2c3RhbA\udcc3\udca1=\n'
        s2 = s.decode('ASCII', errors='surrogateescape')
        self.assertEqual(s2, u)

    @unittest.expectedFailure
    def test_encode_ascii_surrogateescape(self):
        """
        This crops up in the email module. It would be nice if it worked ...
        """
        payload = u'cMO2c3RhbA\udcc3\udca1=\n'
        b = payload.encode('ascii', 'surrogateescape')
        self.assertEqual(b, b'cMO2c3RhbA\xc3\xa1=\n')


class SurrogateEscapeTest(unittest.TestCase):
    """
    These tests are from Python 3.3's test suite
    """
    def setUp(self):
        register_surrogateescape()

    @unittest.expectedFailure
    def test_utf8(self):
        # Bad byte
        self.assertEqual(b"foo\x80bar".decode("utf-8", "surrogateescape"),
                         "foo\udc80bar")
        self.assertEqual("foo\udc80bar".encode("utf-8", "surrogateescape"),
                         b"foo\x80bar")
        # bad-utf-8 encoded surrogate
        self.assertEqual(b"\xed\xb0\x80".decode("utf-8", "surrogateescape"),
                         "\udced\udcb0\udc80")
        self.assertEqual("\udced\udcb0\udc80".encode("utf-8", "surrogateescape"),
                         b"\xed\xb0\x80")

    def test_ascii(self):
        # bad byte
        self.assertEqual(b"foo\x80bar".decode("ascii", "surrogateescape"),
                         "foo\udc80bar")
        # Fails:
        # self.assertEqual("foo\udc80bar".encode("ascii", "surrogateescape"),
        #                  b"foo\x80bar")

    @unittest.expectedFailure
    def test_charmap(self):
        # bad byte: \xa5 is unmapped in iso-8859-3
        self.assertEqual(b"foo\xa5bar".decode("iso-8859-3", "surrogateescape"),
                         "foo\udca5bar")
        self.assertEqual("foo\udca5bar".encode("iso-8859-3", "surrogateescape"),
                         b"foo\xa5bar")

    def test_latin1(self):
        # Issue6373
        self.assertEqual("\udce4\udceb\udcef\udcf6\udcfc".encode("latin-1", "surrogateescape"),
                         b"\xe4\xeb\xef\xf6\xfc")


if __name__ == '__main__':
    unittest.main()
