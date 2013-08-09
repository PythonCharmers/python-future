"""
Note that the Python 2.x round() function fails these tests. The Python 3.x
round() function passes them, as should our custom round() function.

Also tests input()
"""

from __future__ import absolute_import, division

from future.builtins import round

import textwrap
from subprocess import Popen, PIPE, check_output, STDOUT
import unittest


class TestIterators(unittest.TestCase):
    def test_round(self):
        self.assertEqual(round(12.35, 2), 12.35)
        self.assertEqual(round(12.35, 1), 12.3)
        self.assertEqual(round(12.35, 0), 12.0)

        self.assertEqual(round(123.5, 1), 123.5)

        self.assertEqual(round(0.1250, 2), 0.12)
        self.assertEqual(round(0.1350, 2), 0.14)
        self.assertEqual(round(0.1251, 2), 0.13)
        self.assertEqual(round(0.125000001, 2), 0.13)

        self.assertEqual(round(123.5, 0), 124.0)
        self.assertTrue(isinstance(round(123.5, 0), float))

        self.assertEqual(round(123.5), 124)
        self.assertTrue(isinstance(round(123.5), int))

    @unittest.skip('negative exponents not implemented')
    def test_round_negative_exponents(self):
        self.assertEqual(round(12.35, -1), 10.0)
        self.assertEqual(round(12.35, -2), 0.0)
        self.assertEqual(round(123.5, -1), 120.0)
        self.assertEqual(round(123.5, -2), 100.0)
        self.assertEqual(round(123.551, -2), 100.0)
        self.assertEqual(round(123.551, -3), 0.0)

        self.assertEqual(round(10.1350, -1), 10.0)
        self.assertEqual(round(10.1350, -2), 0.0)

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
    unittest.main(failfast=True)
