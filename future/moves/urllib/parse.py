from __future__ import absolute_import
from future.standard_library import suspend_hooks

from urlparse import (ParseResult, SplitResult, parse_qs, parse_qsl,
                      urldefrag, urljoin, urlparse, urlsplit,
                      urlunparse, urlunsplit)

# we use this method to get at the original py2 urllib before any renaming
# quote = sys.py2_modules['urllib'].quote
# quote_plus = sys.py2_modules['urllib'].quote_plus
# unquote = sys.py2_modules['urllib'].unquote
# unquote_plus = sys.py2_modules['urllib'].unquote_plus
# urlencode = sys.py2_modules['urllib'].urlencode
# splitquery = sys.py2_modules['urllib'].splitquery

with suspend_hooks():
    from urllib import (quote,
                        quote_plus,
                        unquote,
                        unquote_plus,
                        urlencode,
                        splitquery)
