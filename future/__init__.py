"""
The ``future`` module helps run Python 3.x-compatible code under Python 2.

It allows people to write clean, modern Python 3.x-compatible code today
and to run it with minimal effort under Python 2 alongside a Python 2
stack that may contain dependencies that have not yet been ported to
Python 3.

It is designed to be used as follows:

    from __future__ import (division, absolute_import, print_function,
                            unicode_string_literals)
    from future import *
    from future import standard_library_renames

followed by clean Python 3 code (with a few restrictions) that can run
unchanged on Python 2.7 or Python 3.3.

The above * import is equivalent to:

    from future.common_iterators import zip, map, filter
    from future.features import range, super
    from future.disable_obsolete_builtins import (apply, cmp, coerce,
            execfile, file, long, raw_input, reduce, reload, unicode,
            xrange, StandardError)
    from future.str_is_unicode import str, python_2_unicode_compatible


See the docstrings for each of these modules for more info:

    future.standard_library_renames
    future.common_iterators
    future.features
    future.disable_obsolete_builtins
    future.str_as_unicode

"""

from __future__ import (division, absolute_import, print_function)

from future.common_iterators import *
from future.features import *
from future.disable_obsolete_builtins import *
from future.str_is_unicode import *


__ver_major__ = 0
__ver_minor__ = 1
__ver_patch__ = 0
__ver_sub__ = ''
__version__ = "%d.%d.%d%s" % (__ver_major__,__ver_minor__,__ver_patch__,__ver_sub__)
VERSION = __version__

# __all__ = ['disable_obsolete_builtins', 'common_iterators', 'str_is_unicode',
#            'standard_library_renames', 'features']

