"""
This tests whether

    from future import *

and

    from future.builtins import *

work as expected. They should NOT introduce namespace pollution. On Python 3,
this should have precisely no effect whatsoever. On Python 2, this should not
introduce any new symbols, but merely shadow some of the builtins.

"""

from __future__ import absolute_import, print_function, unicode_literals

import unittest
import copy

from future import utils

original_locals = set(copy.copy(locals()))
original_globals = set(copy.copy(globals()))
new_names = {'original_locals', 'original_globals', 'new_names'}
from future import *
from future.builtins import *
new_locals = set(copy.copy(locals())) - new_names - original_locals
new_globals = set(copy.copy(globals())) - new_names - original_globals - \
              {'new_locals'}

# from future.tests import (test_common_iterators,
#                           test_super,
#                           test_standard_library_renames,
#                           test_str_is_unicode)

# class TestImportStar(test_common_iterators.TestIterators,
#                      test_super.TestSuper,
#                      test_standard_library_renames.TestStandardLibraryRenames,
#                      test_str_is_unicode.TestStrIsUnicode):

# @unittest.skip('Cannot use "from future import *" within unittest module')
class TestImportStar(unittest.TestCase):
    """
    It would be nice if we could implement this as a subclass as above, to
    avoid duplication. How?
    """
    def test_namespace_pollution_locals(self):
        if utils.PY3:
            self.assertEqual(len(new_locals), 0,
                             'namespace pollution: {}'.format(new_locals))
        else:
            pass   # maybe check that no new symbols are introduced

    def test_namespace_pollution_globals(self):
        if utils.PY3:
            self.assertEqual(len(new_globals), 0,
                             'namespace pollution: {}'.format(new_globals))
        else:
            pass   # maybe check that no new symbols are introduced

    def test_iterators(self):
        self.assertNotEqual(type(range(10)), list)

    def test_super(self):
        pass

    def test_python3_stdlib_imports(self):
        # These should fail on Py2
        import queue
        import socketserver

    def test_str(self):
        self.assertIsNot(str, bytes)            # Py2: assertIsNot only in 2.7
        self.assertEqual(str('blah'), u'blah')  # Py3.3 and Py2 only

    def test_python_2_unicode_compatible_decorator(self):
        # This should not be in the namespace
        assert 'python_2_unicode_compatible' not in locals()


if __name__ == '__main__':
    unittest.main()
