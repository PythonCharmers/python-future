"""
Tests to make sure the behaviour of the builtins is sensible, even with
the future module * imports.
"""

from __future__ import absolute_import, division
from future.builtins import int      # not long
from future import utils

import unittest


class TestBuiltins(unittest.TestCase):
    def test_int(self):
        self.assertTrue(isinstance(0, int))

    @unittest.expectedFailure   # Py2's long doesn't inherit from int!
    def test_long(self):
        self.assertEqual(isinstance(10**100, int))
        if not utils.PY3:
            self.assertEqual(isinstance(long(1), int))
        # Note: the following is a SyntaxError on Py3:
        # self.assertEqual(isinstance(1L, int))


if __name__ == '__main__':
    unittest.main()
