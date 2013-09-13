"""
This module contains snippets of Python 2 code (invalid Python 3) and
tests for whether they can be passed to ``futurize`` and immediately
run under both Python 2 again and Python 3.
"""

from __future__ import print_function, absolute_import

import unittest
import pprint
from subprocess import Popen, PIPE
import tempfile
import os

from future.tests.base import CodeHandler


class TestFuturizeSimple(CodeHandler, unittest.TestCase):
    def setUp(self):
        self.interpreters = ('python', 'python3')
        self.tempdir = tempfile.mkdtemp() + os.path.sep
        self.env = {'PYTHONPATH': os.getcwd()}

    def test_xrange(self):
        code = '''
        for i in xrange(10):
            pass
        '''
        self.simple_convert_and_run(code)

    def test_range_slice(self):
        """
        This should run on Py2 without a MemoryError
        """
        code = '''
        for i in range(10**15)[:10]:
            pass
        '''
        self.simple_convert_and_run(code)

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
        self.simple_convert_and_run(code)

    def test_apply(self):
        code = '''
        def addup(*x):
            return sum(x)
        
        assert apply(addup, (10,20)) == 30
        '''
        self.simple_convert_and_run(code)
    
    def test_renamed_modules(self):
        code = '''
        import ConfigParser
        import copy_reg
        import cPickle
        import cStringIO
        '''
        self.simple_convert_and_run(code)
    
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

        The code is the first snippet from these docs:
            http://docs.python.org/2/library/2to3.html
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

        for interpreter in self.interpreters:
            p1 = Popen([interpreter, self.tempdir + 'mytestscript.py'],
                       stdout=PIPE, stdin=PIPE, stderr=PIPE, env=self.env)
            (stdout, stderr) = p1.communicate(b'Ed')
            # print(stdout)
            # print(stderr)
            self.assertEqual(stdout, b"What's your name?\nHello, Ed!\n")

    def test_u_prefixes_are_not_stripped(self):
        """
        Tests to ensure that the u'' prefixes on unicode strings are not
        removed by the futurize script.  Removing the prefixes on Py3.3+ is
        unnecessary and loses some information -- namely, that the strings have
        explicitly been marked as unicode, rather than just the futurize
        script's guess (perhaps incorrect) that they should be unicode.
        """
        code = '''
        s = u'Hello'
        '''
        newcode = self.simple_convert(code)
        self.assertTrue("s = u'Hello'" in newcode)

        
if __name__ == '__main__':
    unittest.main()
