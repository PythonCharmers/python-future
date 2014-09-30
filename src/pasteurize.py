#!/usr/bin/env python
"""
pasteurize.py
=============

pasteurize.py attempts to turn Py3 code into relatively clean Py3 code that is
also compatible with Py2 when using the ``future`` package.


Licensing
---------
Copyright 2013-2014 Python Charmers Pty Ltd, Australia.
The software is distributed under an MIT licence. See LICENSE.txt.
"""

import os

from libpasteurize.main import main

# We use os._exit() because sys.exit() seems to interact badly with
# subprocess.check_output() ...
os._exit(main())

