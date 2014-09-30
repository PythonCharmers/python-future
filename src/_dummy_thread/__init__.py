from __future__ import absolute_import
import sys
__future_module__ = True

if sys.version_info[0] < 3:
    from dummy_thread import *
else:
    raise ImportError('Cannot import module from python-future source folder')
