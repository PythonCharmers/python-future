"""
Tests for whether the standard library hooks in ``future`` are compatible with
the ``requests`` package.
"""

from __future__ import absolute_import, unicode_literals, print_function
from future import standard_library
from future.tests.base import unittest, CodeHandler
import textwrap
import sys
import os


with standard_library.suspend_hooks():
    try:
        import requests
    except ImportError:
        requests = None


class write_module(object):
    """
    A context manager to streamline the tests. Creates a temp file for a
    module designed to be imported by the ``with`` block, then removes it
    afterwards.
    """
    def __init__(self, code, tempdir):
        self.code = code
        self.tempdir = tempdir

    def __enter__(self):
        print('Creating {0}/test_imports_future_stdlib ...'.format(self.tempdir))
        with open(self.tempdir + 'test_imports_future_stdlib.py', 'w') as f:
            f.write(textwrap.dedent(self.code))
        sys.path.insert(0, self.tempdir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        If an exception occurred, we leave the file for inspection.
        """
        sys.path.remove(self.tempdir)
        if exc_type is None:
            # No exception occurred
            os.remove(self.tempdir + 'test_imports_future_stdlib.py')


class TestRequests(CodeHandler):
    """
    This class tests whether the requests module conflicts with the
    standard library import hooks, as in issue #19.
    """
    @unittest.skipIf(requests is None, 'Install ``requests`` if you would like' \
                     + ' to test ``requests`` + future compatibility (issue #19)')
    def test_requests(self):
        code = """
            from future import standard_library
            standard_library.install_hooks()

            import html.parser
            """
        with write_module(code, self.tempdir):
            import test_imports_future_stdlib
            standard_library.remove_hooks()
            import requests
            r = requests.get('http://google.com')
            self.assertTrue(r)

        # Was:
        # try:
        #    (code)
        # except Exception as e:
        #     raise e
        # else:
        #     print('Succeeded!')
        # finally:
        #     sys.path.remove(self.tempdir)


    @unittest.skipIf(requests is None, 'Install ``requests`` if you would like' \
                     + ' to test ``requests`` + future compatibility (issue #19)')
    def test_requests_cm(self):
        """
        Tests whether requests can be used importing standard_library modules
        previously with the hooks context manager
        """
        code = """
            from future import standard_library
            with standard_library.hooks():
                 import builtins
                 import html.parser
                 import http.client
            """
        with write_module(code, self.tempdir):
            import test_imports_future_stdlib
            import requests
            r = requests.get('http://google.com')
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
