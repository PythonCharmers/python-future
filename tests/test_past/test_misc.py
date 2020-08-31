# -*- coding: utf-8 -*-
"""
Tests for the resurrected Py2-like cmp funtion
"""

from __future__ import absolute_import, unicode_literals, print_function

import os.path
import sys
import traceback

from future.tests.base import unittest
from past.builtins import cmp

_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_dir)
import test_values


class TestCmp(unittest.TestCase):
    def test_cmp(self):
        for x, y, cmp_python2_value in test_values.cmp_python2_value:
            with self.subTest(x=x, y=y):
                try:
                    past_cmp_value = cmp(x, y)
                except Exception as ex:
                    past_cmp_value = traceback.format_exc().strip().split('\n')[-1]

                self.assertEqual(cmp_python2_value, past_cmp_value,
                                 "expected result matching python2 __builtins__.cmp({x!r},{y!r}) "
                                 "== {cmp_python2_value} "
                                 "got past.builtins.cmp({x!r},{y!r}) "
                                 "== {past_cmp_value} "
                                 "".format(x=x, y=y, past_cmp_value=past_cmp_value,
                                           cmp_python2_value=cmp_python2_value))


if __name__ == '__main__':
    unittest.main()
