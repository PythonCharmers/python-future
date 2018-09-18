from __future__ import absolute_import
from future.utils import PY2

from subprocess import *

if PY2:
    __future_module__ = True
    from commands import getoutput, getstatusoutput
