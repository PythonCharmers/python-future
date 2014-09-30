from __future__ import absolute_import
import sys
__future_module__ = True

if sys.version_info[0] == 3:
    from future.standard_library import exclude_local_folder_imports
    with exclude_local_folder_imports('http.server'):
        from http.server import *
else:
    __future_module__ = True
    from BaseHTTPServer import *
    from CGIHTTPServer import *
    from SimpleHTTPServer import *
    try:
        from CGIHTTPServer import _url_collapse_path     # needed for a test
    except ImportError:
        try:
            # Python 2.7.0 to 2.7.3
            from CGIHTTPServer import (
                _url_collapse_path_split as _url_collapse_path)
        except ImportError:
            # Doesn't exist on Python 2.6.x. Ignore it.
            pass
