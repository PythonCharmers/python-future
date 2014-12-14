# -*- coding: utf-8 -*-
"""
Tests for the backported class:`range` class.
"""

from future.builtins import range
from future.tests.base import unittest

from collections import Iterator, Sequence


class RangeTests(unittest.TestCase):
    def test_range(self):
        self.assertTrue(isinstance(range(0), Sequence))
        self.assertTrue(isinstance(reversed(range(0)), Iterator))

    def test_bool_range(self):
        self.assertFalse(range(0))
        self.assertTrue(range(1))
        self.assertFalse(range(1, 1))
        self.assertFalse(range(5, 2))

    def test_equality_range(self):
        self.assertEqual(range(7), range(7))
        self.assertEqual(range(0), range(1, 1))
        self.assertEqual(range(0, 10, 3), range(0, 11, 3))

    def test_slice_empty_range(self):
        self.assertEqual(range(0)[:], range(0))
        self.assertEqual(range(0)[::-1], range(-1, -1, -1))

    def test_slice_range(self):
        r = range(8)
        self.assertEqual(r[:], range(8))
        self.assertEqual(r[:2], range(2))
        self.assertEqual(r[:-2], range(6))
        self.assertEqual(r[2:], range(2, 8))
        self.assertEqual(r[-2:], range(6, 8))
        self.assertEqual(r[2:-2], range(2, 6))
        self.assertEqual(r[-2:2:-1], range(6, 2, -1))
        r = r[::-1]
        self.assertEqual(r, range(7, -1, -1))
        self.assertEqual(r[:], range(7, -1, -1))
        self.assertEqual(r[:2], range(7, 5, -1))
        self.assertEqual(r[:-2], range(7, 1, -1))
        self.assertEqual(r[2:], range(5, -1, -1))
        self.assertEqual(r[-2:], range(1, -1, -1))
        self.assertEqual(r[2:-2], range(5, 1, -1))
        self.assertEqual(r[-2:2:-1], range(1, 5))

    def test_slice_offsetted_range(self):
        r = range(4, 16)
        self.assertEqual(r[:], range(4, 16))
        self.assertEqual(r[::-1], range(15, 3, -1))
        self.assertEqual(r[:4], range(4, 8))
        self.assertEqual(r[:-4], range(4, 12))
        self.assertEqual(r[4:], range(8, 16))
        self.assertEqual(r[-4:], range(12, 16))
        self.assertEqual(r[4:-4], range(8, 12))
        self.assertEqual(r[-4:4:-1], range(12, 8, -1))

    def test_slice_overflow_range(self):
        r = range(8)
        self.assertEqual(r[2:200], range(2, 8))
        self.assertEqual(r[-200:-2], range(0, 6))

    def test_stepped_slice_range(self):
        r = range(8)
        self.assertEqual(r[::2], range(0, 8, 2))
        self.assertEqual(r[::-2], range(7, -1, -2))
        self.assertEqual(r[:2:2], range(0, 2, 2))
        self.assertEqual(r[:-2:2], range(0, 6, 2))
        self.assertEqual(r[2::2], range(2, 8, 2))
        self.assertEqual(r[-2::2], range(6, 8, 2))
        self.assertEqual(r[2:-2:2], range(2, 6, 2))

    def test_stepped_slice_stepped_range(self):
        r = range(0, 16, 2)
        self.assertEqual(r[::2], range(0, 16, 4))
        self.assertEqual(r[:2:2], range(0, 4, 4))
        self.assertEqual(r[:-2:2], range(0, 12, 4))
        self.assertEqual(r[2::2], range(4, 16, 4))
        self.assertEqual(r[-2::2], range(12, 16, 4))
        self.assertEqual(r[2:-2:2], range(4, 12, 4))

    def test_rev_slice_range(self):
        r = range(8)
        self.assertEqual(r[::-1], range(7, -1, -1))
        self.assertEqual(r[:2:-1], range(7, 2, -1))
        self.assertEqual(r[:-2:-1], range(7, 6, -1))
        self.assertEqual(r[2::-1], range(2, -1, -1))
        self.assertEqual(r[-2::-1], range(6, -1, -1))
        self.assertEqual(r[-2:2:-1], range(6, 2, -1))
        r = range(0, 16, 2)
        self.assertEqual(r[::-2], range(14, -2, -4))
        self.assertEqual(r[:2:-2], range(14, 4, -4))
        self.assertEqual(r[:-2:-2], range(14, 12, -4))
        self.assertEqual(r[2::-2], range(4, -2, -4))
        self.assertEqual(r[-2::-2], range(12, -2, -4))
        self.assertEqual(r[-2:2:-2], range(12, 4, -4))

    def test_slice_zero_step(self):
        msg = '^slice step cannot be zero$'
        with self.assertRaisesRegexp(ValueError, msg):
            range(8)[::0]

    def test_properties(self):
        # Exception string differs between PY2/3
        r = range(0)
        with self.assertRaises(AttributeError):
            r.start = 0
        with self.assertRaises(AttributeError):
            r.stop = 0
        with self.assertRaises(AttributeError):
            r.step = 0


if __name__ == '__main__':
    unittest.main()
