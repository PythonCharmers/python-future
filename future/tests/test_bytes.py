# -*- coding: utf-8 -*-
"""
Tests for the backported bytes object
"""

from __future__ import absolute_import, unicode_literals, print_function
from future.builtins import bytes
from future import utils

import unittest

TEST_UNICODE_STR = u'ℝεα∂@ßʟ℮ ☂ℯṧт υηḯ¢☺ḓ℮'
# Tk icon as a .gif:
TEST_BYTE_STR = b'GIF89a\x0e\x00\x0b\x00\x80\xff\x00\xff\x00\x00\xc0\xc0\xc0!\xf9\x04\x01\x00\x00\x01\x00,\x00\x00\x00\x00\x0e\x00\x0b\x00@\x02\x1f\x0c\x8e\x10\xbb\xcan\x90\x99\xaf&\xd8\x1a\xce\x9ar\x06F\xd7\xf1\x90\xa1c\x9e\xe8\x84\x99\x89\x97\xa2J\x01\x00;\x1a\x14\x00;;\xba\nD\x14\x00\x00;;'


class TestBytes(unittest.TestCase):
    def test_bytes_encoding_arg(self):
        """
        The bytes class has changed in Python 3 to accept an
        additional argument in the constructor: encoding.

        It would be nice to support this without breaking the
        isinstance(..., bytes) test below.
        """
        u = u'Unicode string: \u5b54\u5b50'
        b = bytes(u, encoding='utf-8')
        self.assertEqual(b, u.encode('utf-8'))

    def test_bytes_string_no_encoding(self):
        with self.assertRaises(TypeError):
            bytes(u'ABC')

    def test_bytes_int(self):
        """
        In Py3, bytes(int) -> bytes object of size given by the parameter initialized with null
        """
        self.assertEqual(bytes(5), b'\x00\x00\x00\x00\x00')
        # Negative counts are not allowed in Py3:
        with self.assertRaises(ValueError):
            bytes(-1)

    def test_bytes_empty(self):
        """
        bytes() -> b''
        """
        self.assertEqual(bytes(), b'')

    def test_bytes_iterable_of_ints(self):
        self.assertEqual(bytes([65, 66, 67]), b'ABC')

    def test_bytes_bytes(self):
        self.assertEqual(bytes(b'ABC'), b'ABC')

    def test_bytes_fromhex(self):
        self.assertEqual(bytes.fromhex('bb 0f'), b'\xbb\x0f')
        self.assertEqual(bytes.fromhex('1234'), b'\x124')
        self.assertEqual(bytes.fromhex('12ffa0'), b'\x12\xff\xa0')
        b = b'My bytestring'
        self.assertEqual(bytes(b).fromhex('bb 0f'), b'\xbb\x0f')

    def test_isinstance_bytes(self):
        self.assertTrue(isinstance(bytes(b'blah'), bytes))

    @unittest.expectedFailure
    def test_isinstance_oldbytestrings_bytes(self):
        """
        Watch out for this. Byte-strings produced in various places in Py2
        are of type 'str'. With 'from future.builtins import bytes', 'bytes'
        is redefined to be a subclass of 'str', not just an alias for 'str'.
        """
        self.assertTrue(isinstance(b'blah', bytes))   # not with the redefined bytes obj
        self.assertTrue(isinstance(u'blah'.encode('utf-8'), bytes))   # not with the redefined bytes obj

    def test_bytes_getitem(self):
        b = bytes(b'ABCD')
        self.assertEqual(b[0], 65)
        self.assertEqual(b[-1], 68)
        self.assertEqual(b[0:1], b'A')
        self.assertEqual(b[:], b'ABCD')

    @unittest.expectedFailure
    def test_b_literal_creates_newbytes_object(self):
        """
        It would nice if the b'' literal syntax could be coaxed into producing
        bytes objects somehow ... ;)
        """
        b = b'ABCD'
        self.assertTrue(isinstance(b, bytes))
        self.assertEqual(b[0], 65)
        self.assertTrue(repr(b).startswith('b'))

    def test_repr(self):
        b = bytes(b'ABCD')
        self.assertTrue(repr(b).startswith('b'))

    def test_str(self):
        b = bytes(b'ABCD')
        self.assertTrue(str(b), "b'ABCD'")

    def test_bytes_setitem(self):
        b = b'ABCD'
        with self.assertRaises(TypeError):
            b[0] = b'B'

    def test_bytes_iteration(self):
        b = bytes(b'ABCD')
        for item in b:
            self.assertTrue(isinstance(item, int))
        self.assertEqual(list(b), [65, 66, 67, 68])

    def test_bytes_plus_unicode_string(self):
        b = bytes(b'ABCD')
        u = u'EFGH'
        with self.assertRaises(TypeError):
            b + u

        with self.assertRaises(TypeError):
            u + b

    def test_bytes_plus_bytes(self):
        b1 = bytes(b'ABCD')
        b2 = b1 + b1
        self.assertEqual(b2, b'ABCDABCD')
        self.assertTrue(isinstance(b2, bytes))

        b3 = b1 + b'ZYXW'
        self.assertEqual(b3, b'ABCDZYXW')
        self.assertTrue(isinstance(b3, bytes))

        b4 = b'ZYXW' + b1
        self.assertEqual(b4, b'ZYXWABCD')
        self.assertTrue(isinstance(b4, bytes))

    def test_bytes_join_bytes(self):
        b = bytes(b' * ')
        strings = [b'AB', b'EFGH', b'IJKL']
        result = b.join(strings)
        self.assertEqual(result, b'AB * EFGH * IJKL')
        self.assertTrue(isinstance(result, bytes))

    def test_bytes_join_unicode_strings(self):
        b = bytes(b'ABCD')
        strings = [u'EFGH', u'IJKL']
        with self.assertRaises(TypeError):
            b.join(strings)

    def test_bytes_replace(self):
        b = bytes(b'ABCD')
        c = b.replace(b'A', b'F')
        self.assertEqual(c, b'FBCD')
        self.assertTrue(isinstance(c, bytes))

        with self.assertRaises(TypeError):
            b.replace(b'A', u'F')
        with self.assertRaises(TypeError):
            b.replace(u'A', b'F')

    def test_bytes_partition(self):
        b1 = bytes(b'ABCD')
        parts = b1.partition(b'B')
        self.assertEqual(parts, (b'A', b'B', b'CD'))
        self.assertTrue(all([isinstance(p, bytes) for p in parts]))

        b2 = bytes(b'ABCDABCD')
        parts = b2.partition(b'B')
        self.assertEqual(parts, (b'A', b'B', b'CDABCD'))

    def test_bytes_rpartition(self):
        b2 = bytes(b'ABCDABCD')
        parts = b2.rpartition(b'B')
        self.assertEqual(parts, (b'ABCDA', b'B', b'CD'))
        self.assertTrue(all([isinstance(p, bytes) for p in parts]))

    def test_bytes_contains_something(self):
        b = bytes(b'ABCD')
        self.assertTrue(b'A' in b)
        self.assertTrue(65 in b)

        self.assertTrue(b'AB' in b)
        self.assertTrue(bytes([65, 66]) in b)

        self.assertFalse(b'AC' in b)
        self.assertFalse(bytes([65, 67]) in b)

        self.assertFalse(b'Z' in b)
        self.assertFalse(99 in b)

        with self.assertRaises(TypeError):
            u'A' in b

    def test_bytes_index(self):
        b = bytes(b'ABCD')
        self.assertEqual(b.index(b'B'), 1)
        self.assertEqual(b.index(67), 2)

    def test_startswith(self):
        b = bytes(b'abcd')
        self.assertTrue(b.startswith(b'a'))
        self.assertTrue(b.startswith((b'a', b'b')))
        self.assertTrue(b.startswith(bytes(b'ab')))
        self.assertFalse(b.startswith((b'A', b'B')))

        with self.assertRaises(TypeError) as cm:
            b.startswith(65)
        with self.assertRaises(TypeError) as cm:
            b.startswith([b'A'])
        exc = str(cm.exception)
        # self.assertIn('bytes', exc)
        # self.assertIn('tuple', exc)

    def test_endswith(self):
        b = bytes(b'abcd')
        self.assertTrue(b.endswith(b'd'))
        self.assertTrue(b.endswith((b'c', b'd')))
        self.assertTrue(b.endswith(bytes(b'cd')))
        self.assertFalse(b.endswith((b'A', b'B')))

        with self.assertRaises(TypeError) as cm:
            b.endswith(65)
        with self.assertRaises(TypeError) as cm:
            b.endswith([b'D'])
        exc = str(cm.exception)
        # self.assertIn('bytes', exc)
        # self.assertIn('tuple', exc)
        

if __name__ == '__main__':
    unittest.main()
