from __future__ import absolute_import
from future.utils import PY3

if PY3:
    raise ImportError('Cannot import module from python-future source folder')
    from copyreg import *
else:
    __future_module__ = True
    from copy_reg import *
