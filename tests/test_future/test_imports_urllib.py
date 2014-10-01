from __future__ import absolute_import, print_function

import sys
from future.tests.base import unittest

class ImportUrllibTest(unittest.TestCase):
    def test_urllib(self):
        """
        Tests that urllib isn't changed from under our feet. (This might not
        even be a problem?)
        """
        from future import standard_library
        import urllib
        orig_file = urllib.__file__
        with standard_library.hooks():
            import urllib.response
        self.assertEqual(orig_file, urllib.__file__)


if __name__ == '__main__':
    unittest.main()
