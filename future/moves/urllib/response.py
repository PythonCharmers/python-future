from future import standard_library

with standard_library.suspend_hooks():
    from urllib import (addbase,
                        addclosehook,
                        addinfo,
                        addinfourl)

# we use this method to get at the original py2 urllib before any renaming
# addbase = sys.py2_modules['urllib'].addbase
# addclosehook = sys.py2_modules['urllib'].addclosehook
# addinfo = sys.py2_modules['urllib'].addinfo
# addinfourl = sys.py2_modules['urllib'].addinfourl

