from __future__ import absolute_import

from future.standard_library import suspend_hooks

import sys

# We use this method to get at the original Py2 urllib before any renaming magic

pathname2url = sys.py2_modules['urllib'].pathname2url
url2pathname = sys.py2_modules['urllib'].url2pathname
getproxies = sys.py2_modules['urllib'].getproxies
urlretrieve = sys.py2_modules['urllib'].urlretrieve
urlcleanup = sys.py2_modules['urllib'].urlcleanup
URLopener = sys.py2_modules['urllib'].URLopener
FancyURLopener = sys.py2_modules['urllib'].FancyURLopener
proxy_bypass = sys.py2_modules['urllib'].proxy_bypass

with suspend_hooks():
    from urllib2 import (
                     urlopen,
                     install_opener,
                     build_opener,
                     Request,
                     OpenerDirector,
                     HTTPDefaultErrorHandler,
                     HTTPRedirectHandler,
                     HTTPCookieProcessor,
                     ProxyHandler,
                     BaseHandler,
                     HTTPPasswordMgr,
                     HTTPPasswordMgrWithDefaultRealm,
                     AbstractBasicAuthHandler,
                     HTTPBasicAuthHandler,
                     ProxyBasicAuthHandler,
                     AbstractDigestAuthHandler,
                     HTTPDigestAuthHandler,
                     ProxyDigestAuthHandler,
                     HTTPHandler,
                     HTTPSHandler,
                     FileHandler,
                     FTPHandler,
                     CacheFTPHandler,
                     UnknownHandler,
                     HTTPErrorProcessor)

