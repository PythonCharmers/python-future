"""
futurize: automatic conversion to clean 2&3 code using ``python-future``
======================================================================

Like Armin Ronacher's modernize.py, but it attempts to produce clean
standard Python 3 code that runs on both Py2 and Py3 using the ``future``
package.

Use like this:

  $ futurize --verbose mypython2script.py

This will attempt to port the code to standard Py3 code that also
provides Py2 compatibility with the help of the right imports from
``future``. To write the changes to disk, use the -w flag.

Or, to make existing Python 3 code compatible with both Python 2 and 3
using the ``future`` package:

  $ futurize --from3 --verbose mypython3script.py

which removes any Py3-only syntax (e.g. new metaclasses) and adds these
import lines:

    from __future__ import absolute_import
    from __future__ import division
    from __future__ import print_function
    from __future__ import unicode_literals
    import future.standard_library
    from future.builtins import *
"""

from __future__ import (absolute_import, print_function, unicode_literals)
from future.builtins import *
import future.standard_library

import sys
import logging
import optparse

from lib2to3.main import main, warn, StdoutRefactoringTool
from lib2to3 import refactor

from libfuturize.fixes2 import (lib2to3_fix_names, libfuturize_2fix_names)
from libfuturize.fixes3 import libfuturize_3fix_names


def main(args=None):
    """Main program.

    Returns a suggested exit status (0, 1, 2).
    """
    # Set up option parser
    parser = optparse.OptionParser(usage="futurize [options] file|dir ...")
    parser.add_option("-d", "--doctests_only", action="store_true",
                      help="Fix up doctests only")
    parser.add_option("-f", "--fix", action="append", default=[],
                      help="Each FIX specifies a transformation; default: all")
    parser.add_option("-j", "--processes", action="store", default=1,
                      type="int", help="Run 2to3 concurrently")
    parser.add_option("-x", "--nofix", action="append", default=[],
                      help="Prevent a fixer from being run.")
    parser.add_option("-l", "--list-fixes", action="store_true",
                      help="List available transformations")
    parser.add_option("-p", "--print-function", action="store_true",
                      help="Modify the grammar so that print() is a function")
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
    if options.from3:
        fixer_pkg = 'libfuturize.fixes3'
        # avail_fixes = set(refactor.get_fixers_from_package(fixer_pkg))
        # avail_fixes.update(libfuturize_3fix_names)
        avail_fixes = libfuturize_3fix_names
        flags["print_function"] = True
    else:
        fixer_pkg = 'libfuturize.fixes2'
        # avail_fixes = set(refactor.get_fixers_from_package(fixer_pkg))
        avail_fixes = set()
        avail_fixes.update(lib2to3_fix_names)
        avail_fixes.update(libfuturize_2fix_names)

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
    if options.print_function:
        flags["print_function"] = True

    # Set up logging handler
    level = logging.DEBUG if options.verbose else logging.INFO
    logging.basicConfig(format='%(name)s: %(message)s', level=level)

    # Initialize the refactoring tool
    # unwanted_fixes = set(options.nofix)
    unwanted_fixes = set(fixer_pkg + ".fix_" + fix for fix in options.nofix)

    # Remove all fixes except one if the input is already Py3
    explicit = set()
    if options.fix:
        all_present = False
        for fix in options.fix:
            if fix == "all":
                all_present = True
            else:
                explicit.add(fixer_pkg + ".fix_" + fix)
                # explicit.add(fix)
        requested = avail_fixes.union(explicit) if all_present else explicit
    else:
        requested = avail_fixes.union(explicit)
    fixer_names = requested.difference(unwanted_fixes)
    print(explicit)
    rt = StdoutRefactoringTool(sorted(fixer_names), flags, sorted(explicit),
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

