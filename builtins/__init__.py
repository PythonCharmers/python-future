from __future__ import absolute_import
import sys
__future_module__ = True

if sys.version_info[0] < 3:
    from __builtin__ import *
    # Overwrite any old definitions with the equivalent future.builtins ones:
    from future.builtins import *
else:
    from future.standard_library import exclude_local_folder_imports
    with exclude_local_folder_imports('builtins'):
        from builtins import *
