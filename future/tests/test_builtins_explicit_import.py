"""
Tests to make sure that all builtins can be imported explicitly from the
future.builtins namespace.
"""

from __future__ import absolute_import, division, unicode_literals
from future.builtins import (filter, map, zip)
from future.builtins import (ascii, chr, hex, input, isinstance, oct, open)
from future.builtins import (bytes, int, range, round, str, super)
from future.tests.base import unittest


class TestBuiltinsExplicitImport(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
