"""
Example Python 2 code with print statement and raw_input().

Check: does libfuturize automatically handle this?
"""

from __future__ import print_function
from future.builtins import *

def greet(name):
    print("Hello, {0}!".format(name))

print("What's your name?")
name = input()
greet(name)
