"""
futurize: automatic conversion to clean 2&3 code using ``python-future``
======================================================================

Like Armin Ronacher's modernize.py, ``futurize`` attempts to produce clean
standard Python 3 code that runs on both Py2 and Py3.

One pass
--------

Use it like this on Python 2 code:

  $ futurize --verbose mypython2script.py

This will attempt to port the code to standard Py3 code that also
provides Py2 compatibility with the help of the right imports from
``future``. To write the changes to disk, use the -w flag.

Or, to make existing Python 3 code compatible with both Python 2 and 3
using the ``future`` package:

  $ futurize --from3 --verbose mypython3script.py

which removes any Py3-only syntax (e.g. new metaclasses) and adds these
import lines:

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future import standard_library
    from future.builtins import *

To write changes to the files, use the -w flag.

Two stages
----------

The ``futurize`` script can also be called in two separate stages. First:

  $ futurize --stage1 mypython2script.py

This produces more modern Python 2 code that is not yet compatible with Python
3. The tests should still run and the diff should be uncontroversial to apply to
most Python projects that are willing to drop support for Python 2.5 and lower.

After this, the recommended approach is to explicitly mark all strings that must
be byte-strings with a b'' prefix, and then invoke the second stage with:

  $ futurize --stage2 mypython2script.py

This implicitly turns all unadorned string literals into unicode strings (Py3
str) and makes the additional changes needed to support Python 3. This stage
introduces a dependency on ``future`` to restore Py2 support.

If you would prefer instead to mark all your text strings explicitly with u''
prefixes and have all unadorned '' strings converted to byte-strings, use this:

  $ futurize --stage2 --tobytes mypython2script.py

Separate stages are not available (or needed) when converting from Python 3.
"""

from __future__ import (absolute_import, print_function, unicode_literals)
from future import standard_library
from future.builtins import *

import sys
import logging
import optparse

from lib2to3.main import main, warn, StdoutRefactoringTool
from lib2to3 import refactor

from libfuturize.fixes2 import (lib2to3_fix_names_stage1,
                                lib2to3_fix_names_stage2,
                                libfuturize_2fix_names_stage1,
                                libfuturize_2fix_names_stage2)
from libfuturize.fixes3 import libfuturize_3fix_names


def main(args=None):
    """Main program.

    Returns a suggested exit status (0, 1, 2).
    """
    # Set up option parser
    parser = optparse.OptionParser(usage="futurize [options] file|dir ...")
    parser.add_option("-a", "--all-imports", action="store_true",
                      help="Adds all __future__ and future imports to each module")
    parser.add_option("-d", "--doctests_only", action="store_true",
                      help="Fix up doctests only")
    parser.add_option("-b", "--tobytes", action="store_true",
                      help="Convert all unadorned string literals to bytes objects")
    parser.add_option("-1", "--stage1", action="store_true",
                      help="Modernize Python 2 code only; no compatibility with Python 3 (or dependency on ``future``)")
    parser.add_option("-2", "--stage2", action="store_true",
                      help="Take modernized (stage1) code and add a dependency on ``future`` to provide Py3 compatibility.")
    parser.add_option("-0", "--both-stages", action="store_true",
                      help="Apply both stages 1 and 2")
    # parser.add_option("-f", "--fix", action="append", default=[],
    #                   help="Each FIX specifies a transformation; default: all")
    parser.add_option("-j", "--processes", action="store", default=1,
                      type="int", help="Run 2to3 concurrently")
    parser.add_option("-x", "--nofix", action="append", default=[],
                      help="Prevent a fixer from being run.")
    parser.add_option("-l", "--list-fixes", action="store_true",
                      help="List available transformations")
    # parser.add_option("-p", "--print-function", action="store_true",
    #                   help="Modify the grammar so that print() is a function")
    parser.add_option("-v", "--verbose", action="store_true",
                      help="More verbose logging")
    parser.add_option("--no-diffs", action="store_true",
                      help="Don't show diffs of the refactoring")
    parser.add_option("-w", "--write", action="store_true",
                      help="Write back modified files")
    parser.add_option("-n", "--nobackups", action="store_true", default=False,
                      help="Don't write backups for modified files.")
    parser.add_option("--from3", action="store_true", default=False,
                      help="Assume the code is already Python 3 and just "
                           "requires ``__future__`` and ``future`` imports.")

    # Parse command line arguments
    refactor_stdin = False
    flags = {}
    options, args = parser.parse_args(args)
    if options.tobytes:
        raise NotImplementedError('the fixer for this is not yet written. '
                          'Please open an issue on:\n'
                          '   https://github.com/PythonCharmers/python-future\n'
                          'if you need it.')
    if options.from3:
        assert not (options.stage1 or options.stage2)
        fixer_pkg = 'libfuturize.fixes3'
        avail_fixes = libfuturize_3fix_names
        flags["print_function"] = True
    else:
        fixer_pkg = 'libfuturize.fixes2'
        avail_fixes = set()
        if not (options.stage1 or options.stage2):
            options.both_stages = True
        else:
            assert options.both_stages is None
            options.both_stages = False
        if options.stage1 or options.both_stages:
            avail_fixes.update(lib2to3_fix_names_stage1)
            avail_fixes.update(libfuturize_2fix_names_stage1)
        if options.stage2 or options.both_stages:
            avail_fixes.update(lib2to3_fix_names_stage2)
            avail_fixes.update(libfuturize_2fix_names_stage2)

    if not options.write and options.no_diffs:
        warn("not writing files and not printing diffs; that's not very useful")
    if not options.write and options.nobackups:
        parser.error("Can't use -n without -w")
    if options.list_fixes:
        print("Available transformations for the -f/--fix option:")
        for fixname in sorted(avail_fixes):
            print(fixname)
        if not args:
            return 0
    if not args:
        print("At least one file or directory argument required.",
              file=sys.stderr)
        print("Use --help to show usage.", file=sys.stderr)
        return 2
    if "-" in args:
        refactor_stdin = True
        if options.write:
            print("Can't write to stdin.", file=sys.stderr)
            return 2

    # If this option were ever needed, it would probably mean the --from3 flag
    # had been forgotten.
    # if options.print_function:
    #     flags["print_function"] = True

    # Set up logging handler
    level = logging.DEBUG if options.verbose else logging.INFO
    logging.basicConfig(format='%(name)s: %(message)s', level=level)

    # Initialize the refactoring tool
    unwanted_fixes = set(fixer_pkg + ".fix_" + fix for fix in options.nofix)

    # The 'all-imports' option forces adding all imports __future__ and "from
    # future import standard_library", even if they don't seem necessary for
    # the current state of each module. (This can simplify testing, and can
    # reduce the need to think about Py2 compatibility when editing the code
    # further.)
    extra_fixes = set()
    if options.all_imports:
        prefix = 'libfuturize.fixes2.'
        if options.stage1:
            extra_fixes.add(prefix +
                            'fix_add__future__imports_except_unicode_literals')
        else:
            # In case the user hasn't run stage1 for some reason:
            extra_fixes.add(prefix + 'fix_add__future__imports')
            extra_fixes.add(prefix + 'fix_add_future_standard_library_import')
            extra_fixes.add(prefix + 'fix_add_all_future_builtins')

    fixer_names = avail_fixes | extra_fixes - unwanted_fixes

    rt = StdoutRefactoringTool(sorted(fixer_names), flags, set(),
                               options.nobackups, not options.no_diffs)

    # Refactor all files and directories passed as arguments
    if not rt.errors:
        if refactor_stdin:
            rt.refactor_stdin()
        else:
            try:
                rt.refactor(args, options.write, options.doctests_only,
                            options.processes)
            except refactor.MultiprocessingUnsupported:
                assert options.processes > 1
                print("Sorry, -j isn't " \
                      "supported on this platform.", file=sys.stderr)
                return 1
        rt.summarize()

    # Return error status (0 if rt.errors is zero)
    return int(bool(rt.errors))

