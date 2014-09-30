# future.moves package
from __future__ import absolute_import
import sys
__future_module__ = True

TOP_LEVEL_MODULES = ['builtins',
                     'configparser',
                     'copyreg',
                     'html',
                     'http',
                     'queue',
                     'reprlib',
                     'socketserver',
                     'test',
                     'tkinter',
                     'winreg',
                     'xmlrpc',
                     '_dummy_thread',
                     '_markupbase',
                     '_thread',
                    ]

def import_top_level_modules():
    from future.standard_library import exclude_local_folder_imports
    with exclude_local_folder_imports(*TOP_LEVEL_MODULES):
        for m in TOP_LEVEL_MODULES:
            try:
                __import__(m)
            except ImportError:     # e.g. winreg
                pass

if sys.version_info[0] == 3:
    import_top_level_modules()
