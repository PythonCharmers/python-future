"""
This tests whether

    from future import *

works as expected.
"""

from __future__ import absolute_import, print_function, unicode_literals

from future import *
from future.tests import (test_common_iterators,
                          test_super,
                          test_standard_library_renames,
                          test_str_is_unicode)

import unittest

# class TestImportStar(test_common_iterators.TestIterators,
#                      test_super.TestSuper,
#                      test_standard_library_renames.TestStandardLibraryRenames,
#                      test_str_is_unicode.TestStrIsUnicode):

class TestImportStar(unittest.TestCase):
    """
    It would be nice if we could implement this as above, to avoid
    duplication. How?
    """
    def test_iterators(self):
        self.assertNotEqual(type(range(10)), list)

    def test_python3_stdlib_imports(self):
        import queue
        import socketserver

    def test_str(self):
        self.assertIsNot(str, bytes)            # Py2: assertIsNot only in 2.7
        self.assertEqual(str('blah'), u'blah')  # Py3.3 and Py2 only

    def test_python_2_unicode_compatible_decorator(self):
        # With the decorator:
        @str_is_unicode.python_2_unicode_compatible
        class A(object):
            def __str__(self):
                return u'Unicode string: \u5b54\u5b50'
        a = A()
        self.assertEqual(str(a), bytes(a).decode('utf-8'))
        assert len(str(a)) == 18
        from future import six
        if not six.PY3:
            assert hasattr(a, '__unicode__')
        print(str(a))


if __name__ == '__main__':
    unittest.main()
