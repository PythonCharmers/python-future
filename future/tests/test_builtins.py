"""
Tests to make sure the behaviour of the builtins is sensible and correct.
"""

from __future__ import absolute_import, division, unicode_literals
from future.builtins import *
from future.utils import PY3
from future.tests.base import unittest

import textwrap
from subprocess import Popen, PIPE
from numbers import Integral
from decimal import Decimal


class TestBuiltins(unittest.TestCase):
    def test_super(self):
        class verbose_list(list):
            '''
            A class that uses the new simpler super() function
            '''
            def append(self, item):
                print('Adding an item')
                super().append(item)

        l = verbose_list()
        l.append('blah')
        self.assertEqual(l[0], 'blah')
        self.assertEqual(len(l), 1)
        self.assertTrue(isinstance(l, list))

    def test_isinstance_int(self):
        """
        Redefining ``int`` to a ``long`` subclass on Py2 makes this
        test fail unless isinstance() is defined appropriately:
        """
        self.assertTrue(isinstance(0, int))
        self.assertTrue(isinstance(int(1), int))
        self.assertFalse(isinstance(1.0, int))

    def test_isinstance_Integral(self):
        """
        Tests the preferred alternative to the above
        """
        self.assertTrue(isinstance(0, Integral))

    def test_isinstance_long(self):
        """
        Py2's long doesn't inherit from int!
        """
        self.assertTrue(isinstance(10**100, int))
        self.assertTrue(isinstance(int(2**64), int))
        if not PY3:
            self.assertTrue(isinstance(long(1), int))
        # Note: the following is a SyntaxError on Py3:
        # self.assertTrue(isinstance(1L, int))

    def test_isinstance_bytes(self):
        self.assertTrue(isinstance(b'byte-string', bytes))
        self.assertFalse(isinstance(b'byte-string', str))

    def test_isinstance_str(self):
        self.assertTrue(isinstance('string', str))
        self.assertTrue(isinstance(u'string', str))
        self.assertFalse(isinstance(u'string', bytes))

    @unittest.expectedFailure
    def test_type(self):
        """
        The following fails when passed a unicode string on Python
        (including when unicode_literals is in effect) and fails when
        passed a byte-string on Python 3. So type() always wants a native
        string as the first argument.

        TODO: maybe provide a replacement that works identically on Py2/3?
        """
        mytype = type('blah', (dict,), {"old": 1, "new": 2})
        d = mytype()
        self.assertTrue(isinstance(d, mytype))
        self.assertTrue(isinstance(d, dict))

    def test_isinstance_tuple_of_types(self):
        # These two should be equivalent, even if ``int`` is a special
        # backported type.
        label = 1
        self.assertTrue(isinstance(label, (float, Decimal)) or
                        isinstance(label, int))
        self.assertTrue(isinstance(label, (float, Decimal, int)))
        self.assertTrue(isinstance(10**100, (float, Decimal, int)))

        self.assertTrue(isinstance(b'blah', (str, bytes)))
        self.assertTrue(isinstance(b'blah', (bytes, float, int)))

        self.assertFalse(isinstance(b'blah', (str, Decimal, float, int)))

        self.assertTrue(isinstance('blah', (str, Decimal, float, int)))
        self.assertTrue(isinstance(u'blah', (Decimal, float, int, str)))

        self.assertFalse(isinstance('blah', (bytes, Decimal, float, int)))

    @unittest.skipIf(sys.version_info[:2] == (2, 6),
                     'not yet implemented for Py2.6')
    def test_round(self):
        """
        Note that the Python 2.x round() function fails these tests. The
        Python 3.x round() function passes them, as should our custom
        round() function.
        """
        self.assertEqual(round(0.1250, 2), 0.12)
        self.assertEqual(round(0.1350, 2), 0.14)
        self.assertEqual(round(0.1251, 2), 0.13)
        self.assertEqual(round(0.125000001, 2), 0.13)
        self.assertEqual(round(123.5, 0), 124.0)
        self.assertEqual(round(123.5), 124)
        self.assertEqual(round(12.35, 2), 12.35)
        self.assertEqual(round(12.35, 1), 12.3)
        self.assertEqual(round(12.35, 0), 12.0)
        self.assertEqual(round(123.5, 1), 123.5)

        self.assertTrue(isinstance(round(123.5, 0), float))
        self.assertTrue(isinstance(round(123.5), Integral))

    @unittest.skip('negative ndigits not implemented yet')
    def test_round_negative_ndigits(self):
        self.assertEqual(round(10.1350, 0), 10.0)
        self.assertEqual(round(10.1350, -1), 10.0)
        self.assertEqual(round(10.1350, -2), 0.0)
        self.assertEqual(round(10.1350, -3), 0.0)

        self.assertEqual(round(12.35, -1), 10.0)
        self.assertEqual(round(12.35, -2), 0.0)
        self.assertEqual(round(123.5, -1), 120.0)
        self.assertEqual(round(123.5, -2), 100.0)
        self.assertEqual(round(123.551, -2), 100.0)
        self.assertEqual(round(123.551, -3), 0.0)

    def test_input(self, interpreter='python2'):
        """
        Passes in a string to the waiting input()
        """
        code = '''
        from future.builtins import input
        def greet(name):
            print "Hello, {0}!".format(name)
        print "What's your name?"
        name = input()
        greet(name)
        '''
        with open('mytestscript.py', 'w') as f:
            f.write(textwrap.dedent(code))
        p1 = Popen([interpreter, 'mytestscript.py'], stdout=PIPE, stdin=PIPE, stderr=None)
        (stdout, stderr) = p1.communicate(b'Ed')
        # print(stdout)
        # print(stderr)
        self.assertEqual(stdout, b"What's your name?\nHello, Ed!\n")


if __name__ == '__main__':
    unittest.main()
