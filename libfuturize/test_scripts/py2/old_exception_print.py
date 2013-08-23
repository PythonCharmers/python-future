"""
Test of whether futurize handles the old-style exception Syntax
"""

from __future__ import print_function
from future.builtins import *

def hello():
    try:
        print("Hello, world")
    except IOError as e:
        print(e.errno)
