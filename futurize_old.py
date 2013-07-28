"""
For the ``future`` package.

Like modernize.py, but it spits out code that *should* be Py2 and Py3
compatible while using the ``future`` package.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
import copy

from lib2to3.main import main

skip_fixes = [
              'buffer',
              'callable',
              'future',
              'metaclass',
              # 'lib2to3.fixes.fix_operator',  - what is this?
             ]
orig_args = copy.copy(sys.argv)

for fix in reversed(skip_fixes):
    sys.argv.insert(1, '--nofix=' + fix)
print(sys.argv)
# sys.exit(0)
status = main("lib2to3.fixes")
if status:
    sys.exit(status)

sys.argv = orig_args
status2 = main("libfuturize.fixes")
sys.exit(status2)

