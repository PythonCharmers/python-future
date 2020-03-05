# -*- coding: utf-8 -*-
"""
Tests for the Py2-like class:`basestring` type.
"""

from __future__ import absolute_import, unicode_literals, print_function
import os

from past import utils
from future.tests.base import unittest
from past.builtins import basestring, str as oldstr


class TestBaseString(unittest.TestCase):

    def test_isinstance(self):
        s = b'abc'
        self.assertTrue(isinstance(s, basestring))
        s2 = oldstr(b'abc')
        self.assertTrue(isinstance(s2, basestring))

    def test_issubclass(self):
        self.assertTrue(issubclass(str, basestring))
        self.assertTrue(issubclass(bytes, basestring))
        self.assertTrue(issubclass(basestring, basestring))
        self.assertFalse(issubclass(int, basestring))
        self.assertFalse(issubclass(list, basestring))
        self.assertTrue(issubclass(basestring, object))

        class CustomString(basestring):
            pass
        class NotString(object):
            pass
        class OldStyleClass:
            pass
        self.assertTrue(issubclass(CustomString, basestring))
        self.assertFalse(issubclass(NotString, basestring))
        self.assertFalse(issubclass(OldStyleClass, basestring))



if __name__ == '__main__':
    unittest.main()
