"""
This tests whether explicit imports like

    from future import str

all work as expected on both Python 2 and Python 3.

"""

from __future__ import absolute_import, print_function, unicode_literals

import unittest
import copy

from future import six

class TestExplicitImports(unittest.TestCase):
    def test_py3_builtin_imports(self):
        from future import (input,
                            filter,
                            map,
                            range,
                            round,
                            super,
                            str,
                            zip)

    def test_py2k_disabled_builtins(self):
        """
        On Py2 these should import.
        """
        if not six.PY3:
            from future import (apply,
                                cmp,
                                coerce,
                                execfile,
                                file,
                                long,
                                raw_input,
                                reduce,
                                reload,
                                unicode,
                                xrange,
                                StandardError)


if __name__ == '__main__':
    unittest.main()
