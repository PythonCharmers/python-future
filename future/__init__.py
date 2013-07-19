"""
The ``future`` module helps run Python 3.x-compatible code under Python 2.

It allows people to write clean, modern Python 3.x-compatible code today and to
run it with minimal effort under Python 2 alongside a Python 2 stack that may
contain dependencies that have not yet been ported to Python 3.

It is designed to be used as follows:

    from __future__ import division, absolute_import, print_function
    from future import common_iterators, super, disable_obsolete_builtins

Eventually, we may also support this:
    from future import standard_library

to bring in the new module names from the Python 3 standard library.
"""

from __future__ import division, absolute_import, print_function

__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 1
__ver_sub__ = ''
__version__ = "%d.%d.%d%s" % (__ver_major__,__ver_minor__,__ver_patch__,__ver_sub__)
VERSION = __version__

__all__ = ['disable_obsolete_builtins', 'common_iterators', 'str_is_unicode']

