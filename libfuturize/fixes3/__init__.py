import sys
from lib2to3 import refactor

# The original set of these fixes comes from lib3to2 (https://bitbucket.org/amentajo/lib3to2):
libfuturize_3fix_names = set([
                            'libfuturize.fixes2.fix_add__future__imports',  # from __future__ import absolute_import etc. on separate lines
                            'libfuturize.fixes2.fix_add_future_standard_library_import',  # we force adding this import for now, even if it doesn't seem necessary to the fix_future_standard_library fixer, for ease of testing
                            'libfuturize.fixes2.fix_order___future__imports',  # consolidates to a single line to simplify testing
                            'libfuturize.fixes3.fix_future_builtins',   # adds "from future.builtins import *"
                            'libfuturize.fixes2.fix_future_standard_library', # adds "from future import standard_library"

                            'libfuturize.fixes3.fix_annotations',
                            # 'libfuturize.fixes3.fix_bitlength',  # ints have this in Py2.7
                            # 'libfuturize.fixes3.fix_bool',    # need a decorator or Mixin
                            # 'libfuturize.fixes3.fix_bytes',   # leave bytes as bytes
                            # 'libfuturize.fixes3.fix_classdecorator',  # available in
                            # Py2.6+
                            # 'libfuturize.fixes3.fix_collections', hmmm ...
                            # 'libfuturize.fixes3.fix_dctsetcomp',  # avail in Py27
                            'libfuturize.fixes3.fix_division',   # yes
                            # 'libfuturize.fixes3.fix_except',   # avail in Py2.6+
                            # 'libfuturize.fixes3.fix_features',  # ?
                            'libfuturize.fixes3.fix_fullargspec',
                            # 'libfuturize.fixes3.fix_funcattrs',
                            'libfuturize.fixes3.fix_getcwd',
                            'libfuturize.fixes3.fix_imports',   # adds "from future import standard_library"
                            'libfuturize.fixes3.fix_imports2',
                            # 'libfuturize.fixes3.fix_input',
                            # 'libfuturize.fixes3.fix_int',
                            # 'libfuturize.fixes3.fix_intern',
                            # 'libfuturize.fixes3.fix_itertools',
                            'libfuturize.fixes3.fix_kwargs',   # yes, we want this
                            # 'libfuturize.fixes3.fix_memoryview',
                            # 'libfuturize.fixes3.fix_metaclass',  # write a custom handler for
                            # this
                            # 'libfuturize.fixes3.fix_methodattrs',  # __func__ and __self__ seem to be defined on Py2.7 already
                            'libfuturize.fixes3.fix_newstyle',   # yes, we want this: explicit inheritance from object. Without new-style classes in Py2, super() will break etc.
                            # 'libfuturize.fixes3.fix_next',   # use a decorator for this
                            # 'libfuturize.fixes3.fix_numliterals',   # prob not
                            # 'libfuturize.fixes3.fix_open',   # huh?
                            # 'libfuturize.fixes3.fix_print',  # no way
                            'libfuturize.fixes3.fix_printfunction',  # adds __future__ import print_function
                            'libfuturize.fixes3.fix_raise',   # yes, if 'raise E, V, T' is supported on Py3
                            # 'libfuturize.fixes3.fix_range',  # nope
                            # 'libfuturize.fixes3.fix_reduce',
                            # 'libfuturize.fixes3.fix_setliteral',
                            # 'libfuturize.fixes3.fix_str',
                            # 'libfuturize.fixes3.fix_super',  # maybe, if our magic super() isn't robust enough
                            'libfuturize.fixes3.fix_throw',   # yes, if Py3 supports it
                            # 'libfuturize.fixes3.fix_unittest',
                            'libfuturize.fixes3.fix_unpacking',  # yes, this is useful
                            # 'libfuturize.fixes3.fix_with'      # way out of date
                           ])

