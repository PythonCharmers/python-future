"""
Miscellaneous function (re)definitions from the Py3.3 standard library for
Python 2.6/2.7.
"""
from math import ceil as oldceil

def ceil(x):
    """
    Return the ceiling of x as an int.
    This is the smallest integral value >= x.
    """
    return int(oldceil(x))
