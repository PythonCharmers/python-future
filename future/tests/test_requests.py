# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import pprint
import tempfile
import os
from subprocess import Popen, PIPE

from future.tests.base import CodeHandler, unittest


class TestRequests(CodeHandler):
    """
    This class tests whether the requests module conflicts with the
    standard library import hooks, as in issue #19.
    """
    import sys
    print('sys.meta_path is: ', sys.meta_path)
    print('Importing test_imports_future')
    import test_imports_future
    import requests
    r = requests.get('http://google.com')
