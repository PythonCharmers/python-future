from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future.standard_library.email import policy
from future.tests.base import unittest
from future.tests.test_email import TestEmailBase


class Test(TestEmailBase):

    policy = policy.default

    def test_error_on_setitem_if_max_count_exceeded(self):
        m = self._str_msg("")
        m['To'] = 'abc@xyz'
        with self.assertRaises(ValueError):
            m['To'] = 'xyz@abc'


if __name__ == '__main__':
    unittest.main()
