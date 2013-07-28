"""
For the ``future`` package.

Like modernize.py, but it spits out code that *should* be Py2 and Py3
compatible while using the ``future`` package.

Use like this to port Python 2 code:

  $ python futurize.py --verbose mypython2script.py

and try to auto-backport it by adding ``future`` module imports.

Or, to make existing Python 3 code compatible with Python 2 using the
``future`` package:

  $ python futurize.py --from3 --verbose mypython3script.py

which just adds these import lines:

    from __future__ import absolute_import
    from __future__ import division
    from __future__ import print_function
    from __future__ import unicode_literals
    import future.standard_library_renames
    from future import *
    # other imports here

to invoke the 3rd-party ``future`` package to provide Py2 compatibility.
"""

import sys
import logging
import optparse

from lib2to3.main import main, warn, StdoutRefactoringTool
from lib2to3 import refactor

from libfuturize.fixes import (lib2to3_fix_names, future_package_fix_names)


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

    fixer_pkg = 'libfuturize.fixes'
    avail_fixes = set(refactor.get_fixers_from_package(fixer_pkg))
    avail_fixes.update(lib2to3_fix_names)
    avail_fixes.update(future_package_fix_names)

    # Parse command line arguments
    refactor_stdin = False
    flags = {}
    options, args = parser.parse_args(args)
    if not options.write and options.no_diffs:
        warn("not writing files and not printing diffs; that's not very useful")
    if not options.write and options.nobackups:
        parser.error("Can't use -n without -w")
    if options.list_fixes:
        print "Available transformations for the -f/--fix option:"
        for fixname in sorted(avail_fixes):
            print fixname
        if not args:
            return 0
    if not args:
        print >> sys.stderr, "At least one file or directory argument required."
        print >> sys.stderr, "Use --help to show usage."
        return 2
    if "-" in args:
        refactor_stdin = True
        if options.write:
            print >> sys.stderr, "Can't write to stdin."
            return 2
    if options.print_function:
        flags["print_function"] = True

    # Set up logging handler
    level = logging.DEBUG if options.verbose else logging.INFO
    logging.basicConfig(format='%(name)s: %(message)s', level=level)

    # Initialize the refactoring tool
    unwanted_fixes = set(options.nofix)

    # Remove all fixes except one if the input is already Py3
    explicit = set()
    if options.from3:
        fixer_names = {'libfuturize.fixes.fix_future_package'}
    else:
        if options.fix:
            all_present = False
            for fix in options.fix:
                if fix == "all":
                    all_present = True
                else:
                    explicit.add(fix)
            requested = avail_fixes.union(explicit) if all_present else explicit
        else:
            requested = avail_fixes.union(explicit)
        fixer_names = requested.difference(unwanted_fixes)
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
                print >> sys.stderr, "Sorry, -j isn't " \
                    "supported on this platform."
                return 1
        rt.summarize()

    # Return error status (0 if rt.errors is zero)
    return int(bool(rt.errors))

