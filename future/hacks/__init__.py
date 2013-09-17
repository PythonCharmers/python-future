"""
Modifications to builtin objects on Py2 to provide better Py3 compatibility.
"""
from future.hacks.hacktools import hackclass, get_dict

__all__ = ['hackclass', 'hackedlong', 'hackedbytes']
