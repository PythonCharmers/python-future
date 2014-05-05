from future import standard_library
from future.utils import PY3

if PY3:
    from urllib.response import *
else:
    with standard_library.suspend_hooks():
        from urllib import (addbase,
                            addclosehook,
                            addinfo,
                            addinfourl)

