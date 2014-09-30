from __future__ import absolute_import
import sys

if sys.version_info[0] < 3:
    from ConfigParser import *
else:
    from future.standard_library import exclude_local_folder_imports
    with exclude_local_folder_imports('configparser'):
        from configparser import *
