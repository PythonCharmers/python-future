"""
This disables builtin functions (and one exception class) which are removed
from Python 3.3.

This module is designed to be used like this:

    from future import disable_obsolete_builtins

We don't hack __builtin__, which is very fragile because it contaminates
imported modules too. Instead, we just create new global functions with the
same names as the obsolete builtins from Python 2 which raise exceptions when
called.

The following functions are disabled:

    apply, cmp, coerce, execfile, file, raw_input,
    long, unicode, xrange

and this exception class:

    StandardError

(Note that callable() is not among them; this was reintroduced into Python
3.2.)

Also to do:
- Fix round()
- Fix input()
- Fix int()
"""

from __future__ import division, absolute_import, print_function

import inspect

from . import six

OBSOLETE_BUILTINS = ['apply', 'cmp', 'coerce', 'execfile', 'file',
                     'raw_input', 'long', 'unicode', 'xrange',
                     'StandardError']

def disabled_function(name):
    '''
    Returns a function that cannot be called
    '''
    def disabled(*args, **kwargs):
        raise NotImplementedError('obsolete Python 2 builtin {} is disabled'.format(name))
    return disabled

if not six.PY3:
    caller = inspect.currentframe().f_back
    
    for fname in OBSOLETE_BUILTINS:
        def disabled(*args, **kwargs):
            raise NotImplementedError('obsolete Python 2 builtin {} is disabled'.format(fname))
        caller.f_globals.__setitem__(fname, disabled_function(fname))

