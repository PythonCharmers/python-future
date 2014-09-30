#!/usr/bin/env python
"""
futurize.py
===========

This script is only used by the unit tests. Another script called
"futurize" is created automatically (without the .py extension) by
setuptools.

futurize.py attempts to turn Py2 code into valid, clean Py3 code that is
also compatible with Py2 when using the ``future`` package.


Licensing
---------
Copyright 2013 Python Charmers Pty Ltd, Australia.
The software is distributed under an MIT licence. See LICENSE.txt.
"""

import os

from libfuturize.main import main

# We use os._exit() because sys.exit() seems to interact badly with
# subprocess.check_output() ...
os._exit(main())

