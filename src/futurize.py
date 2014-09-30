#!/usr/bin/env python
"""
futurize.py
===========

Like Armin Ronacher's ``modernize.py``, but using the ``future`` package rather than a direct dependency on ``six``'.

futurize.py attempts to turn Py2 code into valid, clean Py3 code that is also
compatible with Py2 when using the ``future`` package.


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

