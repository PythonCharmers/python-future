from __future__ import absolute_import
import sys
__future_module__ = True

if sys.version_info[0] < 3:
    from repr import *
else:
    from future.standard_library import exclude_local_folder_imports
    with exclude_local_folder_imports('reprlib'):
        from reprlib import *
