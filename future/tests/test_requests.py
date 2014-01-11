from __future__ import print_function
import sys
print('sys.meta_path is: ', sys.meta_path)
print('Importing test_imports_future')
import test_imports_future
import requests
r = requests.get('http://google.com')
