from __future__ import absolute_import, print_function

import sys
from future.tests.base import unittest

class ImportUrllibTest(unittest.TestCase):
    def test_urllib(self):
        import urllib
        orig_file = urllib.__file__
        from future.standard_library.urllib import response as urllib_response
        self.assertEqual(orig_file, urllib.__file__)
        print(urllib_response.__file__)

if __name__ == '__main__':
    unittest.main()
