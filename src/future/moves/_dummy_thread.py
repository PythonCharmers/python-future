from __future__ import absolute_import
from future.utils import PY3

if PY3:
    # _dummy_thread and dummy_threading modules were both deprecated in
    # Python 3.7 and removed in Python 3.9
    try:
        from _dummy_thread import *
    except ImportError:
        from _thread import *
else:
    __future_module__ = True
    from dummy_thread import *
