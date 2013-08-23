"""
This tests whether futurize keeps the old two-argument super() calls the
same as before. It should, because this still works in Py3.
"""
from __future__ import print_function
from future.builtins import *

class VerboseList(list):
    def append(self, item):
        print('Adding an item')
        super(VerboseList, self).append(item)
