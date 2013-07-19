from __future__ import absolute_import

from future import str_is_unicode

import unittest

class TestIterators(unittest.TestCase):
    def test_str(self):
        self.assertIsNot(str, bytes)            # Py2: assertIsNot only in 2.7
        self.assertEqual(str('blah'), u'blah')  # Py3.3 and Py2 only

unittest.main()
