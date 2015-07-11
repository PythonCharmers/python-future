# -*- coding: utf-8 -*-
"""
Tests for various backported functions and classes in ``future.backports``
"""

from __future__ import absolute_import, unicode_literals, print_function

from future.backports.misc import count, _count
from future.utils import PY26
from future.tests.base import unittest, skip26


class CountTest(unittest.TestCase):
    """Test the count function."""

    def _test_count_func(self, func):
        self.assertEqual(next(func(1)), 1)
        self.assertEqual(next(func(start=1)), 1)

        c = func()
        self.assertEqual(next(c), 0)
        self.assertEqual(next(c), 1)
        self.assertEqual(next(c), 2)
        c = func(1, 1)
        self.assertEqual(next(c), 1)
        self.assertEqual(next(c), 2)
        c = func(step=1)
        self.assertEqual(next(c), 0)
        self.assertEqual(next(c), 1)
        c = func(start=1, step=1)
        self.assertEqual(next(c), 1)
        self.assertEqual(next(c), 2)

        c = func(-1)
        self.assertEqual(next(c), -1)
        self.assertEqual(next(c), 0)
        self.assertEqual(next(c), 1)
        c = func(1, -1)
        self.assertEqual(next(c), 1)
        self.assertEqual(next(c), 0)
        self.assertEqual(next(c), -1)
        c = func(-1, -1)
        self.assertEqual(next(c), -1)
        self.assertEqual(next(c), -2)
        self.assertEqual(next(c), -3)

    def test_count(self):
        """Test the count function."""
        self._test_count_func(count)

    def test_own_count(self):
        """Test own count implementation."""
        if PY26:
            self.assertIs(count, _count)
        else:
            self.assertNotEqual(count, _count)
            self._test_count_func(_count)


if __name__ == '__main__':
    unittest.main()
