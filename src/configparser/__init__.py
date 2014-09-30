from __future__ import absolute_import
import sys

if sys.version_info[0] < 3:
    from ConfigParser import *
else:
    raise ImportError('Cannot import module from python-future source folder')
