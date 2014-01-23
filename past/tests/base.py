# An abbreviated version of future/tests/base.py

import os
import tempfile
import unittest
if not hasattr(unittest, 'skip'):
    import unittest2 as unittest

from textwrap import dedent
import subprocess

# For Python 2.6 compatibility: see http://stackoverflow.com/questions/4814970/
if "check_output" not in dir(subprocess): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f


