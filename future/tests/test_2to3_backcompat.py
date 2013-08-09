"""
This module contains snippets of Python 2 code (invalid Python 3) and
tests for whether they can be passed to 2to3 and immediately under Python
with the future module using::
    
    from future.builtins import *

It contains tests that perform a scripted porting process using
``futurize``. It then tests whether the resulting Python 2/3 code is
indeed able to run under Python 3 and under Python 2 using the relevant
``future`` module imports.
"""

from __future__ import print_function, absolute_import

import unittest
import textwrap
import pprint
from subprocess import Popen, PIPE
import tempfile
import os

from future.tests.base import CodeHandler


class Test2to3Simple(CodeHandler, unittest.TestCase):
    def setUp(self):
        self.interpreter = 'python'
        self.tempdir = tempfile.mkdtemp() + os.path.sep
        self.env = {'PYTHONPATH': os.getcwd()}

    def test_xrange(self):
        code = '''
        for i in xrange(10):
            pass
        '''
        self.simple_convert_and_check(code)

    def test_range_slice(self):
        """
        This should run on Py2 without a MemoryError
        """
        code = '''
        for i in range(10**15)[:10]:
            pass
        '''
        self.simple_convert_and_check(code)

    def test_super(self):
        """
        Ensure the old method of calling super() still works.
        """
        code = '''
        class VerboseList(list):
            def append(self, item):
                print 'Adding an item'
                super(VerboseList, self).append(item)
        '''
        self.simple_convert_and_check(code)

    def test_apply(self):
        code = '''
        def addup(*x):
            return sum(x)
        
        assert apply(addup, (10,20)) == 30
        '''
        self.simple_convert_and_check(code)
    
    def test_renamed_modules(self):
        code = '''
        import ConfigParser
        import copy_reg
        import cPickle
        import cStringIO
        '''
        self.simple_convert_and_check(code)
    
    def simple_convert_and_check(self, code):
        """
        Tests a complete conversion of this simple piece of code from the
        docs here:
            http://docs.python.org/2/library/2to3.html
        and whether 2to3 can be applied and then the resulting code be
        automatically run under Python 2 with the future module.
        """
        # Translate the clean source file, then add our imports
        self._write_test_script(code)
        self._futurize_test_script()
        output2 = self._run_test_script()
        print(output2)

    @unittest.skip('not implemented yet')
    def test_download_pypi_package_and_test(self, package_name='future'):
        URL = 'http://pypi.python.org/pypi/{}/json'
        
        from future import standard_library
        import requests
        r = requests.get(URL.format(package_name))
        pprint.pprint(r.json())
        
        download_url = r.json()['urls'][0]['url']
        filename = r.json()['urls'][0]['filename']
        # r2 = requests.get(download_url)
        # with open('/tmp/' + filename, 'w') as tarball:
        #     tarball.write(r2.content)

        # Ideally, we'd be able to use code like this:
        # import urllib.request
        # 
        # r = urllib.request.urlopen(URL.format(package_name))
        # pprint.pprint(r.read()) 

    def test_raw_input(self):
        """
        Passes in a string to the waiting input() after futurize
        conversion.
        """
        py2code = '''
        from future.builtins import *
        def greet(name):
            print "Hello, {0}!".format(name)
        print "What's your name?"
        name = raw_input()
        greet(name)
        '''
        self._write_test_script(py2code)
        output = self._futurize_test_script()
        # print(output)

        p1 = Popen([self.interpreter, self.tempdir + 'mytestscript.py'],
                   stdout=PIPE, stdin=PIPE, stderr=PIPE, env=self.env)
        (stdout, stderr) = p1.communicate(b'Ed')
        print(stdout)
        print(stderr)
        self.assertEqual(stdout, b"What's your name?\nHello, Ed!\n")

        
if __name__ == '__main__':
    unittest.main()
