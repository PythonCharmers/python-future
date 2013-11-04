import sys
from lib2to3 import refactor

# The following fixers are "safe": they convert Python 2 code to more
# modern Python 2 code. They should be uncontroversial to apply to most
# projects that are happy to drop support for Py2.5 and below. Applying
# them first will reduce the size of the patch set for the real porting.
lib2to3_fix_names_stage1 = set([
    'lib2to3.fixes.fix_apply',
    'lib2to3.fixes.fix_except',
    'lib2to3.fixes.fix_execfile',
    'lib2to3.fixes.fix_exitfunc',
    'lib2to3.fixes.fix_funcattrs',
    'lib2to3.fixes.fix_filter',
    'lib2to3.fixes.fix_has_key',
    'lib2to3.fixes.fix_idioms',
    # 'lib2to3.fixes.fix_import',    # makes any implicit relative imports explicit. (Use with ``from __future__ import absolute_import)
    'lib2to3.fixes.fix_intern',
    'lib2to3.fixes.fix_isinstance',
    'lib2to3.fixes.fix_methodattrs',
    'lib2to3.fixes.fix_ne',
    'lib2to3.fixes.fix_numliterals',    # turns 1L into 1, 0755 into 0o755
    'lib2to3.fixes.fix_paren',
    # 'lib2to3.fixes.fix_print',
    # 'lib2to3.fixes.fix_raise',   # uses incompatible with_traceback() method on exceptions
    'lib2to3.fixes.fix_renames',
    'lib2to3.fixes.fix_reduce',
    # 'lib2to3.fixes.fix_set_literal',  # this is unnecessary and breaks Py2.6 support
    'lib2to3.fixes.fix_repr',
    'lib2to3.fixes.fix_standarderror',
    'lib2to3.fixes.fix_sys_exc',
    'lib2to3.fixes.fix_throw',
    'lib2to3.fixes.fix_tuple_params',
    'lib2to3.fixes.fix_types',
    'lib2to3.fixes.fix_ws_comma',
    'lib2to3.fixes.fix_xreadlines',
])

# The following fixers add a dependency on the ``future`` package on order to
# support Python 2:
lib2to3_fix_names_stage2 = set([
    'lib2to3.fixes.fix_basestring',
    # 'lib2to3.fixes.fix_buffer',    # perhaps not safe. Test this.
    # 'lib2to3.fixes.fix_callable',  # not needed in Py3.2+
    'lib2to3.fixes.fix_dict',        # TODO: add support for utils.viewitems() etc.
    'lib2to3.fixes.fix_exec',
    # 'lib2to3.fixes.fix_future',    # we don't want to remove __future__ imports
    'lib2to3.fixes.fix_getcwdu',
    # 'lib2to3.fixes.fix_imports',   # called by libfuturize.fixes2.fix_future_standard_library
    # 'lib2to3.fixes.fix_imports2',  # we don't handle this yet (dbm)
    'lib2to3.fixes.fix_input',
    'lib2to3.fixes.fix_itertools',
    'lib2to3.fixes.fix_itertools_imports',
    'lib2to3.fixes.fix_long',
    'lib2to3.fixes.fix_map',
    # 'lib2to3.fixes.fix_metaclass', # causes SyntaxError in Py2! Use the one from ``six`` instead
    'lib2to3.fixes.fix_next',
    'lib2to3.fixes.fix_nonzero',     # TODO: add a decorator for mapping __bool__ to __nonzero__
    'lib2to3.fixes.fix_operator',    # we will need support for this by e.g. extending the Py2 operator module to provide those functions in Py3
    'lib2to3.fixes.fix_raw_input',
    # 'lib2to3.fixes.fix_unicode',   # strips off the u'' prefix, which removes a potentially helpful source of information for disambiguating unicode/byte strings
    'lib2to3.fixes.fix_urllib',
    'lib2to3.fixes.fix_xrange',
    'lib2to3.fixes.fix_zip',
])

libfuturize_2fix_names_stage1 = set([
    'libfuturize.fixes2.fix_absolute_import',
    'libfuturize.fixes2.fix_division',
    'libfuturize.fixes2.fix_print_with_import',
    'libfuturize.fixes2.fix_raise',
    'libfuturize.fixes2.fix_order___future__imports',  # TODO: consolidate to a single line to simplify testing
])

libfuturize_2fix_names_stage2 = set([
    'libfuturize.fixes2.fix_future_builtins',
    'libfuturize.fixes2.fix_future_standard_library',
    'libfuturize.fixes2.fix_metaclass',
   # TODO: add int(33243) calls for what used to be 33243L
    'libfuturize.fixes2.fix_order___future__imports',  # TODO: consolidate to a single line to simplify testing
    'libfuturize.fixes2.fix_unicode_keep_u',
    'libfuturize.fixes2.fix_unicode_literals_import',
])

