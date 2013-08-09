'''
Tests for the new super() function syntax
'''
from __future__ import absolute_import, print_function
from future.builtins.backports import super

import unittest


class TestSuper(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
