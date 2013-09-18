"""
Experimental tools for modifying builtin objects on Py2 to provide better Py3
compatibility. Hopefully none of these will be needed ... ;)
"""
from future.hacks.hacktools import hackclass, get_dict
from future.hacks.hackedbytes import hackedbytes
from future.hacks.hackedlong import hackedlong

__all__ = ['hackclass', 'hackedlong', 'hackedbytes']
