"""
This module contains snippets of Python 3 code (invalid Python 2) and
tests for whether they can be passed to ``futurize --from3`` and immediately
run under both Python 2 and Python 3.
"""

from __future__ import print_function, absolute_import

import pprint
from subprocess import Popen, PIPE
import tempfile
import os

from future.tests.base import CodeHandler, unittest


class TestFuturizeFrom3(CodeHandler):
    def test_range_slice(self):
        """
        After running ``futurize --from3``, this Python 3 code should run on
        both Py3 and Py2 without a MemoryError
        """
        code = '''
        for i in range(10**15)[:10]:
            pass
        '''
        self.unchanged(code, from3=True)

    def test_print(self):
        """
        This Python 3-only code is a SyntaxError on Py2 without the
        print_function import from __future__.
        """
        code = '''
        import sys
        print('Hello', file=sys.stderr)
        '''
        self.unchanged(code, from3=True)

    def test_division(self):
        """
        True division should not be screwed up by conversion from 3 to both
        """
        code = '''
        x = 3 / 2
        assert x == 1.5
        '''
        self.unchanged(code, from3=True)


class TestFuturizeAnnotations(CodeHandler):
    @unittest.expectedFailure
    def test_return_annotations_alone(self):
        before = "def foo() -> 'bar': pass"
        after = """
        def foo(): pass
        foo.__annotations__ = {'return': 'bar'}
        """
        self.check(before, after, from3=True)

        b = """
        def foo() -> "bar":
            print "baz"
            print "what's next, again?"
        """
        a = """
        def foo():
            print "baz"
            print "what's next, again?"
        """
        self.check(b, a, from3=True)

    @unittest.expectedFailure
    def test_single_param_annotations(self):
        b = "def foo(bar:'baz'): pass"
        a = """
        def foo(bar): pass
        foo.__annotations__ = {'bar': 'baz'}
        """
        self.check(b, a, from3=True)

        b = """
        def foo(bar:"baz"="spam"):
            print("what's next, again?")
            print("whatever.")
        """
        a = """
        def foo(bar="spam"):
            print("what's next, again?")
            print("whatever.")
        foo.__annotations__ = {'bar': 'baz'}
        """
        self.check(b, a, from3=True)

    @unittest.expectedFailure
    def test_multiple_param_annotations(self):
        b = "def foo(bar:'spam'=False, baz:'eggs'=True, ham:False='spaghetti'): pass"
        a = "def foo(bar=False, baz=True, ham='spaghetti'): pass"
        self.check(b, a, from3=True)

        b = """
        def foo(bar:"spam"=False, baz:"eggs"=True, ham:False="spam"):
            print("this is filler, just doing a suite")
            print("suites require multiple lines.")
        """
        a = """
        def foo(bar=False, baz=True, ham="spam"):
            print("this is filler, just doing a suite")
            print("suites require multiple lines.")
        """
        self.check(b, a, from3=True)

    @unittest.expectedFailure
    def test_mixed_annotations(self):
        b = "def foo(bar=False, baz:'eggs'=True, ham:False='spaghetti') -> 'zombies': pass"
        a = "def foo(bar=False, baz=True, ham='spaghetti'): pass"
        self.check(b, a, from3=True)

        b = """
        def foo(bar:"spam"=False, baz=True, ham:False="spam") -> 'air':
            print("this is filler, just doing a suite")
            print("suites require multiple lines.")
        """
        a = """
        def foo(bar=False, baz=True, ham="spam"):
            print("this is filler, just doing a suite")
            print("suites require multiple lines.")
        """
        self.check(b, a, from3=True)

        b = "def foo(bar) -> 'brains': pass"
        a = "def foo(bar): pass"
        self.check(b, a, from3=True)

    def test_functions_unchanged(self):
        s = "def foo(): pass"
        self.unchanged(s, from3=True)

        s = """
        def foo():
            pass
            pass
        """
        self.unchanged(s, from3=True)

        s = """
        def foo(bar='baz'):
            pass
            pass
        """
        self.unchanged(s, from3=True)
        

if __name__ == '__main__':
    unittest.main()
