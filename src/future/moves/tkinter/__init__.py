from __future__ import absolute_import
from future.utils import PY3
__future_module__ = True

if not PY3:
    from Tkinter import *
    from Tkinter import _flatten, _cnfmerge
else:
    from tkinter import *
