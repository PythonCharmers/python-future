from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
import unittest
from email import policy
from test.test_email import TestEmailBase


class Test(TestEmailBase):

    policy = policy.default

    def test_error_on_setitem_if_max_count_exceeded(self):
        m = self._str_msg("")
        m['To'] = 'abc@xyz'
        with self.assertRaises(ValueError):
            m['To'] = 'xyz@abc'


if __name__ == '__main__':
    unittest.main()
