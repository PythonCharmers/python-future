"""
This module contains snippets of Python 2 code (invalid Python 3) and
tests for whether they can be passed to 2to3 and immediately under Python
with the future module using:

    from future import *

It contains tests that perform a scripted porting process using 2to3.
(and in the future also python-modernize). It then tests whether the
resulting Python 2/3 code (python-modernize) or Python 3 code (from 2to3)
is able to run under Python 2 using the relevant ``future`` module
imports.
"""

from __future__ import print_function, absolute_import

import unittest
import textwrap
import pprint
from subprocess import Popen, PIPE, check_output, STDOUT


class Test2to3Simple(unittest.TestCase):
    def setUp(self):
        self.interpreter = 'python'

    def test_xrange(self):
        code = '''
        for i in xrange(10):
            pass
        '''
        self.simple_convert_and_check(code)

    def test_range_slice(self):
        code = '''
        for i in range(10**11)[:10]:
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
        self.simple_convert_and_check(code, fixers=['print'])

    def test_apply(self):
        code = '''
        def addup(*x):
            return sum(x)
        
        assert apply(addup, (10,20)) == 30
        '''
        self.simple_convert_and_check(code, fixers=['apply'])
    
    def test_renamed_modules(self):
        code = '''
        import ConfigParser
        import copy_reg
        import cPickle
        import cStringIO
        '''
        self.simple_convert_and_check(code, fixers=['imports'])
    
    def simple_convert_and_check(self, code, fixers=['all']):
        """
        Tests a complete conversion of this simple piece of code from the
        docs here:
            http://docs.python.org/2/library/2to3.html
        and whether 2to3 can be applied and then the resulting code be
        automatically run under Python 2 with the future module.
        """
        # Translate the clean source file, then add our imports
        with open('mytestscript.py', 'w') as f:
            f.write(textwrap.dedent(code))
        output = check_output(['2to3', 'mytestscript.py', '-w', '-f'] + fixers,
                              stderr=STDOUT)
        # print(output)
        # Read the translated file and add our imports
        with open('mytestscript.py') as f:
            newsource = f.read()
        with open('mytestscript.py', 'w') as f:
            f.write('from __future__ import print_function, absolute_import, division, unicode_literals\n')
            f.write('from future import *\n')
            f.write('from future import standard_library_renames\n')
            f.write(newsource)

        output2 = check_output([self.interpreter, 'mytestscript.py'])
        print(output2)

    @unittest.skip('not implemented yet')
    def test_download_pypi_package_and_test(self, package_name='future'):
        URL = 'http://pypi.python.org/pypi/{}/json'
        
        from future import standard_library_renames
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
        Passes in a string to the waiting input() after 2to3 conversion
        """
        code = '''
        from future import *
        def greet(name):
            print "Hello, {0}!".format(name)
        print "What's your name?"
        name = raw_input()
        greet(name)
        '''
        with open('mytestscript.py', 'w') as f:
            f.write(textwrap.dedent(code))
        output = check_output(['2to3', 'mytestscript.py', '-w'],
                              stderr=STDOUT)
        # print(output)
        p1 = Popen([self.interpreter, 'mytestscript.py'],
                   stdout=PIPE, stdin=PIPE)
        (stdout, stderr) = p1.communicate(b'Ed')
        print(stdout)
        #print(stderr)
        self.assertEqual(stdout, b"What's your name?\nHello, Ed!\n")

        
if __name__ == '__main__':
    unittest.main()
