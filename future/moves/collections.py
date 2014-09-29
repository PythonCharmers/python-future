from __future__ import absolute_import

from collections import *

from future.utils import PY2, PY26

if PY2:
    from UserDict import UserDict
    from UserList import UserList
    from UserString import UserString

if PY26:
    from future.backports.misc import OrderedDict, Counter
