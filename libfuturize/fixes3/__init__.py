import sys
from lib2to3 import refactor

libfuturize_3fix_names = set([
                            'fix_annotations',
                            # 'fix_bitlength',  # ints have this in Py2.7
                            # 'fix_bool',    # need a decorator or Mixin
                            # 'fix_bytes',   # leave bytes as bytes
                            # 'fix_classdecorator',  # available in
                            # Py2.6+
                            # 'fix_collections', hmmm ...
                            # 'fix_dctsetcomp',  # avail in Py27
                            'fix_division',   # yes
                            # 'fix_except',   # avail in Py2.6+
                            # 'fix_features',  # ?
                            'fix_fullargspec',
                            # 'fix_funcattrs',
                            'fix_getcwd',
                            # 'fix_imports',
                            # 'fix_imports2',
                            # 'fix_input',
                            # 'fix_int',
                            # 'fix_intern',
                            # 'fix_itertools',
                            'fix_kwargs',   # yes, we want this
                            # 'fix_memoryview',
                            # 'fix_metaclass',  # write a custom handler for
                            # this
                            # 'fix_methodattrs',  # __func__ and __self__ seem to be defined on Py2.7 already
                            'fix_newstyle',   # yes, we want this. Without new-style classes in Py2, super() will break etc.
                            # 'fix_next',   # use a decorator for this
                            # 'fix_numliterals',   # prob not
                            # 'fix_open',   # huh?
                            # 'fix_print',  # no way
                            'fix_printfunction',  # adds __future__ import print_function
                            'fix_raise',   # yes, if 'raise E, V, T' is supported on Py3
                            # 'fix_range',  # nope
                            # 'fix_reduce',
                            # 'fix_setliteral',
                            # 'fix_str',
                            # 'fix_super',  # maybe, if our magic super() isn't robust enough
                            'fix_throw',   # yes, if Py3 supports it
                            # 'fix_unittest',
                            'fix_unpacking',  # yes, this is useful
                            # 'fix_with'      # way out of date
                           ])

