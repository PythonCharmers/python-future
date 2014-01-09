# coding=utf-8
"""
past: an implementation of Python 2 constructs in Python 3
==========================================================

``past`` is a package to aid with Python 2/3 compatibility. Whereas ``future``
contains backports of Python 3 constructs to Python 2, ``past`` provides
implementations of some Python 2 constructs in Python 3. It is intended to be
used sparingly, primarily for libraries:

- as a step in porting a Python 2 codebase to Python 3 (e.g. with the ``futurize`` script)
- to provide Python 3 support for previously Python 2-only libraries with the
  same APIs as on Python 2 -- particularly with regard to 8-bit strings (the
  ``past.builtins.str`` type).
- to aid in providing minimal-effort Python 3 support for applications using
  libraries that do not yet wish to upgrade their code properly to Python 3, or
  wish to upgrade it gradually to Python 3 style.


Here are some examples that run identically on Python 3 and 2::

    >>> from past.builtins import str as py2str

    >>> confucius = py2str(b'\xe5\xad\x94\xe5\xad\x90')
    >>> # This now behaves like a Py2 byte-string on both Py2 and Py3.
    >>> # For example, indexing returns a Python 2-like string object, not
    >>> # an integer:
    >>> confucius[0]
    '\xe5'
    >>> type(confucius[0])
    <past.builtins.oldstr>

    >>> # The div() function behaves like Python 2's / operator
    >>> # without "from __future__ import division"
    >>> from past.utils import div
    >>> div(3, 2)    # like 3/2 in Py2
    0
    >>> div(3, 2.0)  # like 3/2.0 in Py2
    1.5

    >>> # List-producing versions of range, reduce, map, filter
    >>> from past.builtins import range, reduce
    >>> range(10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
    15

    >>> # Other functions removed in Python 3 are resurrected ...
    >>> from past.builtins import execfile
    >>> execfile('myfile.py')

    >>> from past.builtins import raw_input
    >>> name = raw_input('What is your name? ')
    What is your name? [cursor]

    >>> from past.builtins import reload
    >>> reload(mymodule)   # equivalent to imp.reload(mymodule) in Python 3

    >>> from past.builtins import xrange
    >>> for i in xrange(10):
    ...     pass



Credits
-------

:Author:  Ed Schofield
:Sponsor: Python Charmers Pty Ltd, Australia, and Python Charmers Pte
          Ltd, Singapore. http://pythoncharmers.com


Licensing
---------
Copyright 2013-2014 Python Charmers Pty Ltd, Australia.
The software is distributed under an MIT licence. See LICENSE.txt.

"""

# from past.builtins import *

__title__ = 'past'
__author__ = 'Ed Schofield'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Python Charmers Pty Ltd'
__ver_major__ = 0
__ver_minor__ = 11
__ver_patch__ = 0
__ver_sub__ = '-dev'
__version__ = "%d.%d.%d%s" % (__ver_major__, __ver_minor__,
                              __ver_patch__, __ver_sub__)


