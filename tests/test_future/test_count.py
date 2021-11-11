# -*- coding: utf-8 -*-
"""
Tests for the backported class:`range` class.
"""
from itertools import count as it_count

from future.backports.misc import count
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

    @skip26
    def test_own_count(self):
        """Test own count implementation."""
        self._test_count_func(it_count)


if __name__ == '__main__':
    unittest.main()
