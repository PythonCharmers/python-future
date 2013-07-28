"""
For the ``future`` package.

Like modernize.py, but it spits out code that *should* be Py2 and Py3
compatible while using the ``future`` package.
"""
import sys

from libfuturize.main import main
sys.exit(main())

