from __future__ import absolute_import
from future.utils import PY3

if PY3:
    from http.cookies import *
else:
    from Cookie import *
    from Cookie import Morsel    # left out of __all__ on Py2.7!
