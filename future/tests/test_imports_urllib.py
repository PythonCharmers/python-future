from __future__ import absolute_import, print_function

import unittest
import sys
# print([m for m in sys.modules if m.startswith('urllib')])

class ImportUrllibTest(unittest.TestCase):
    @unittest.expectedFailure
    def test_urllib(self):
        """
        This will fail: importing urllib first means that the import hooks
        won't be consulted when importing urllib.response.
        """
        import urllib
        print(urllib.__file__)
        from future import standard_library
        with standard_library.hooks():
            import urllib.response
        print(urllib.__file__)
        print(urllib.response.__file__)

unittest.main()
