# -*- coding: utf-8 -*-
"""
Tests for the backported bytes object
"""

from __future__ import absolute_import, unicode_literals, print_function
from future.builtins import *
from future import utils

from numbers import Integral
from future.tests.base import unittest


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
        # Test using newint:
        self.assertEqual(bytes(int(5)), b'\x00\x00\x00\x00\x00')
        self.assertTrue(isinstance(bytes(int(5)), bytes))

        # Negative counts are not allowed in Py3:
        with self.assertRaises(ValueError):
            bytes(-1)
        with self.assertRaises(ValueError):
            bytes(int(-1))

    @unittest.skipIf(utils.PY3, 'test not needed on Py3: all ints are long')
    def test_bytes_long(self):
        """
        As above, but explicitly feeding in a long on Py2. Note that
        checks like:
            isinstance(n, int)
        are fragile on Py2, because isinstance(10L, int) is False.
        """
        m = long(5)
        n = long(-1)
        self.assertEqual(bytes(m), b'\x00\x00\x00\x00\x00')
        # Negative counts are not allowed in Py3:
        with self.assertRaises(ValueError):
            bytes(n)

    def test_bytes_empty(self):
        """
        bytes() -> b''
        """
        self.assertEqual(bytes(), b'')

    def test_bytes_iterable_of_ints(self):
        self.assertEqual(bytes([65, 66, 67]), b'ABC')
        self.assertEqual(bytes([int(120), int(121), int(122)]), b'xyz')

    def test_bytes_bytes(self):
        self.assertEqual(bytes(b'ABC'), b'ABC')

    def test_bytes_is_bytes(self):
        b = bytes(b'ABC')
        self.assertTrue(bytes(b) is b)
        self.assertEqual(repr(bytes(b)), "b'ABC'")

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
            self.assertTrue(isinstance(item, Integral))
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

    def test_bytes_join_others(self):
        b = bytes(b' ')
        with self.assertRaises(TypeError):
            b.join([42])
        with self.assertRaises(TypeError):
            b.join(b'blah')
        with self.assertRaises(TypeError):
            b.join(bytes(b'blah'))

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
        
    def test_decode(self):
        b = bytes(b'abcd')
        s = b.decode('utf-8')
        self.assertEqual(s, 'abcd')
        self.assertTrue(isinstance(s, str))

    def test_encode(self):
        b = bytes(b'abcd')
        with self.assertRaises(AttributeError) as cm:
            b.encode('utf-8')

    def test_eq(self):
        """
        Equals: ==
        """
        b = bytes(b'ABCD')
        self.assertEqual(b, b'ABCD')
        self.assertTrue(b == b'ABCD')
        self.assertEqual(b'ABCD', b)
        self.assertEqual(b, b)
        self.assertFalse(b == b'ABC')
        self.assertFalse(b == bytes(b'ABC'))
        self.assertFalse(b == u'ABCD')
        self.assertFalse(b == str('ABCD'))
        # Fails:
        # self.assertFalse(u'ABCD' == b)
        self.assertFalse(str('ABCD') == b)

        self.assertFalse(b == list(b))
        self.assertFalse(b == str(b))
        self.assertFalse(b == u'ABC')
        self.assertFalse(bytes(b'Z') == 90)

    def test_ne(self):
        b = bytes(b'ABCD')
        self.assertFalse(b != b)
        self.assertFalse(b != b'ABCD')
        self.assertTrue(b != b'ABCDEFG')
        self.assertTrue(b != bytes(b'ABCDEFG'))
        self.assertTrue(b'ABCDEFG' != b)

        # self.assertTrue(b'ABCD' != u'ABCD')
        self.assertTrue(b != u'ABCD')
        self.assertTrue(b != u'ABCDE')
        self.assertTrue(bytes(b'') != str(u''))
        self.assertTrue(str(u'') != bytes(b''))

        self.assertTrue(b != list(b))
        self.assertTrue(b != str(b))

    def test_hash(self):
        d = {}
        b = bytes(b'ABCD')
        native_b = b'ABCD'
        s = str('ABCD')
        native_s = u'ABCD'
        d[b] = b
        d[s] = s
        self.assertEqual(len(d), 2)
        # This should overwrite d[s] but not d[b]:
        d[native_s] = native_s
        self.assertEqual(len(d), 2)
        # This should overwrite d[native_s] again:
        d[s] = s
        self.assertEqual(len(d), 2)
        self.assertEqual(set(d.keys()), set([s, b]))
    
    @unittest.expectedFailure
    def test_hash_with_native_types(self):
        # Warning: initializing the dict with native Py2 types throws the
        # hashing out:
        d = {u'ABCD': u'ABCD', b'ABCD': b'ABCD'}
        # On Py2: len(d) == 1
        b = bytes(b'ABCD')
        s = str('ABCD')
        d[s] = s
        d[b] = b
        # Fails:
        self.assertEqual(len(d) > 1)

    def test_add(self):
        b = bytes(b'ABC')
        c = bytes(b'XYZ')
        d = b + c
        self.assertTrue(isinstance(d, bytes))
        self.assertEqual(d, b'ABCXYZ')
        f = b + b'abc'
        self.assertTrue(isinstance(f, bytes))
        self.assertEqual(f, b'ABCabc')
        g = b'abc' + b
        self.assertTrue(isinstance(g, bytes))
        self.assertEqual(g, b'abcABC')

    def test_cmp(self):
        b = bytes(b'ABC')
        with self.assertRaises(TypeError):
            b > 3
        with self.assertRaises(TypeError):
            b > u'XYZ'
        with self.assertRaises(TypeError):
            b <= 3
        with self.assertRaises(TypeError):
            b >= int(3)
        with self.assertRaises(TypeError):
            b < 3.3
        with self.assertRaises(TypeError):
            b > (3.3 + 3j)
        with self.assertRaises(TypeError):
            b >= (1, 2)
        with self.assertRaises(TypeError):
            b <= [1, 2]

    def test_mul(self):
        b = bytes(b'ABC')
        c = b * 4
        self.assertTrue(isinstance(c, bytes))
        self.assertEqual(c, b'ABCABCABCABC')
        d = b * int(4)
        self.assertTrue(isinstance(d, bytes))
        self.assertEqual(d, b'ABCABCABCABC')
        if utils.PY2:
            e = b * long(4)
            self.assertTrue(isinstance(e, bytes))
            self.assertEqual(e, b'ABCABCABCABC')

    def test_rmul(self):
        b = bytes(b'XYZ')
        c = 3 * b
        self.assertTrue(isinstance(c, bytes))
        self.assertEqual(c, b'XYZXYZXYZ')
        d = b * int(3)
        self.assertTrue(isinstance(d, bytes))
        self.assertEqual(d, b'XYZXYZXYZ')
        if utils.PY2:
            e = long(3) * b
            self.assertTrue(isinstance(e, bytes))
            self.assertEqual(e, b'XYZXYZXYZ')

    def test_slice(self):
        b = bytes(b'ABCD')
        c1 = b[:]
        self.assertTrue(isinstance(c1, bytes))
        self.assertTrue(c1 == b)
        # The following is not true, whereas it is true normally on Py2 and
        # Py3. Does this matter?:
        # self.assertTrue(c1 is b)

        c2 = b[10:]
        self.assertTrue(isinstance(c2, bytes))
        self.assertTrue(c2 == bytes(b''))
        self.assertTrue(c2 == b'')

        c3 = b[:0]
        self.assertTrue(isinstance(c3, bytes))
        self.assertTrue(c3 == bytes(b''))
        self.assertTrue(c3 == b'')

        c4 = b[:1]
        self.assertTrue(isinstance(c4, bytes))
        self.assertTrue(c4 == bytes(b'A'))
        self.assertTrue(c4 == b'A')

        c5 = b[:-1]
        self.assertTrue(isinstance(c5, bytes))
        self.assertTrue(c5 == bytes(b'ABC'))
        self.assertTrue(c5 == b'ABC')


if __name__ == '__main__':
    unittest.main()
