# -*- coding: utf-8 -*-
"""
Tests for the future.str_is_unicode module
"""

from __future__ import absolute_import, unicode_literals, print_function
from future import str_is_unicode

from future import six

import unittest


class TestStrIsUnicode(unittest.TestCase):
    def test_str(self):
        self.assertIsNot(str, bytes)            # Py2: assertIsNot only in 2.7
        self.assertEqual(str('blah'), u'blah')  # Py3.3 and Py2 only

    def test_python_2_unicode_compatible_decorator(self):
        # With the decorator:
        @str_is_unicode.python_2_unicode_compatible
        class A(object):
            def __str__(self):
                return u'Unicode string: \u5b54\u5b50'
        a = A()
        self.assertEqual(str(a), bytes(a).decode('utf-8'))
        assert len(str(a)) == 18
        if not six.PY3:
            assert hasattr(a, '__unicode__')
        print(str(a))

        # Manual equivalent without the decorator:
        class B(object):
            def __unicode__(self):
                return u'Unicode string: \u5b54\u5b50'
            def __str__(self):
                return unicode(self).encode('utf-8')
        b = B()
        assert str(a) == str(b)


unittest.main()
