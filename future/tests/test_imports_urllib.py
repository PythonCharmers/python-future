from __future__ import absolute_import, print_function

import unittest
import sys

class ImportUrllibTest(unittest.TestCase):
    def test_urllib(self):
        """
        This should perhaps fail: importing urllib first means that the import hooks
        won't be consulted when importing urllib.response.
        """
        import urllib
        print(urllib.__file__)
        from future import standard_library
        with standard_library.hooks():
            import urllib.response
        print(urllib.__file__)
        print(urllib.response.__file__)

if __name__ == '__main__':
    unittest.main()
