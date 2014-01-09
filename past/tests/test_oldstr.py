# -*- coding: utf-8 -*-
"""
Tests for the resurrected Py2-like 8-bit string object
"""

from __future__ import absolute_import, unicode_literals, print_function

from numbers import Integral
from future.tests.base import unittest
from past.builtins.types.oldstr import oldstr, collapse_double_backslashes


class TestOldStr(unittest.TestCase):
    def test_repr(self):
        s1 = oldstr(b'abc')
        assert repr(s1) == "'abc'"
        s2 = oldstr(b'abc\ndef')
        assert repr(s2) == "'abc\\ndef'"

    def test_str(self):
        s1 = oldstr(b'abc')
        assert str(s1) == 'abc'
        s2 = oldstr(b'abc\ndef')
        assert str(s2) == 'abc\ndef'

    def test_collapse_double_backslashes(s):
        s = collapse_double_backslashes(r'a\\b\c\\d')   # i.e. 'a\\\\b\\c\\\\d'
        assert str(s) == r'a\b\c\d'
        s2 = collapse_double_backslashes(r'abc\\ndef')   # i.e. 'abc\\\\ndef'
        assert str(s2) == r'abc\ndef'

    def test_getitem(self):
        s = oldstr(b'abc')

        assert s[0] != 97
        assert s[0] == b'a'
        assert s[0] == oldstr(b'a')

        assert s[1:] == b'bc'
        assert s[1:] == oldstr(b'bc')


if __name__ == '__main__':
    unittest.main()
