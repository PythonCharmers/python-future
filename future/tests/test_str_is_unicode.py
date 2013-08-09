# -*- coding: utf-8 -*-
"""
Tests for the future.str_is_unicode module
"""

from __future__ import absolute_import, unicode_literals, print_function
from future.builtins.str_is_unicode import str
from future.utils import python_2_unicode_compatible
from future import utils

import unittest

TEST_UNICODE_STR = u'ℝεα∂@ßʟ℮ ☂ℯṧт υηḯ¢☺ḓ℮'


class TestStrIsUnicode(unittest.TestCase):
    def test_str(self):
        self.assertIsNot(str, bytes)            # Py2: assertIsNot only in 2.7
        self.assertEqual(str('blah'), u'blah')  # u'' prefix: Py3.3 and Py2 only

    def test_str_encode_decode(self):
        a = u'Unicode string: \u5b54\u5b50'
        self.assertEqual(str(a), a.encode('utf-8').decode('utf-8'))

    @unittest.expectedFailure  # on Python 2
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

    def test_isinstance_bytes(self):
        self.assertEqual(isinstance(b'blah', bytes), True)

    def test_python_2_unicode_compatible_decorator(self):
        my_unicode_str = u'Unicode string: \u5b54\u5b50'
        # With the decorator:
        @python_2_unicode_compatible
        class A(object):
            def __str__(self):
                return my_unicode_str
        a = A()
        assert len(str(a)) == 18
        if not utils.PY3:
            assert hasattr(a, '__unicode__')
        self.assertEqual(str(a), my_unicode_str)
        self.assertTrue(isinstance(str(a).encode('utf-8'), bytes))

        # Manual equivalent on Py2 without the decorator:
        if not utils.PY3:
            class B(object):
                def __unicode__(self):
                    return u'Unicode string: \u5b54\u5b50'
                def __str__(self):
                    return unicode(self).encode('utf-8')
            b = B()
            assert str(a) == str(b)


if __name__ == '__main__':
    unittest.main()
