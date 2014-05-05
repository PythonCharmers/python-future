from __future__ import absolute_import

from future.standard_library import suspend_hooks

# We use this method to get at the original Py2 urllib before any renaming magic

# pathname2url = sys.py2_modules['urllib'].pathname2url
# url2pathname = sys.py2_modules['urllib'].url2pathname
# getproxies = sys.py2_modules['urllib'].getproxies
# urlretrieve = sys.py2_modules['urllib'].urlretrieve
# urlcleanup = sys.py2_modules['urllib'].urlcleanup
# URLopener = sys.py2_modules['urllib'].URLopener
# FancyURLopener = sys.py2_modules['urllib'].FancyURLopener
# proxy_bypass = sys.py2_modules['urllib'].proxy_bypass

with suspend_hooks():
    from urllib import *
    from urllib2 import *
    from urlparse import *

    # from urllib import (pathname2url,
    #                     url2pathname,
    #                     getproxies,
    #                     urlretrieve,
    #                     urlcleanup,
    #                     URLopener,
    #                     FancyURLopener,
    #                     proxy_bypass)

    # from urllib2 import (
    #                  AbstractBasicAuthHandler,
    #                  AbstractDigestAuthHandler,
    #                  BaseHandler,
    #                  CacheFTPHandler,
    #                  FileHandler,
    #                  FTPHandler,
    #                  HTTPBasicAuthHandler,
    #                  HTTPCookieProcessor,
    #                  HTTPDefaultErrorHandler,
    #                  HTTPDigestAuthHandler,
    #                  HTTPErrorProcessor,
    #                  HTTPHandler,
    #                  HTTPPasswordMgr,
    #                  HTTPPasswordMgrWithDefaultRealm,
    #                  HTTPRedirectHandler,
    #                  HTTPSHandler,
    #                  URLError,
    #                  build_opener,
    #                  install_opener,
    #                  OpenerDirector,
    #                  ProxyBasicAuthHandler,
    #                  ProxyDigestAuthHandler,
    #                  ProxyHandler,
    #                  Request,
    #                  UnknownHandler,
    #                  urlopen,
    #                 )

    # from urlparse import (
    #                  urldefrag
    #                  urljoin,
    #                  urlparse,
    #                  urlunparse,
    #                  urlsplit,
    #                  urlunsplit,
    #                  parse_qs,
    #                  parse_q"
    #                 )
