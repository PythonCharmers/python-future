"""
This disables builtin functions (and one exception class) which are
removed from Python 3.3.

This module is designed to be used like this:

    from future import disable_obsolete_builtins

We don't hack __builtin__, which is very fragile because it contaminates
imported modules too. Instead, we just create new global functions with
the same names as the obsolete builtins from Python 2 which raise
exceptions when called.

The following functions are disabled:

    apply, cmp, coerce, execfile, file, input, long,
    raw_input, reduce, reload, unicode, xrange

Note that both input() and raw_input() are disabled. Although input()
exists as a builtin in Python 3, the Python 2 input() builtin is unsafe
to use because it can lead to shell injection. Therefore we shadow it by
default, in case someone forgets to import our replacement input()
somehow and expects Python 3 semantics.

Fortunately, input() seems to be seldom used in the wild in Python 2, so
we could probably even delete it from __builtin__... TODO: test this.

(Note that callable() is not among the functions disabled; this was
reintroduced into Python 3.2.)

This exception class is also disabled:

    StandardError

"""

from __future__ import division, absolute_import, print_function

from future import six


OBSOLETE_BUILTINS = ['apply', 'chr', 'cmp', 'coerce', 'execfile', 'file',
                     'input', 'long', 'raw_input', 'reduce', 'reload',
                     'unicode', 'xrange', 'StandardError']


def disabled_function(name):
    '''
    Returns a function that cannot be called
    '''
    def disabled(*args, **kwargs):
        '''
        A function disabled by the ``future`` module. This function is
        no longer a builtin in Python 3.
        '''
        raise NameError('obsolete Python 2 builtin {} is disabled'.format(name))
    return disabled


if not six.PY3:
    for fname in OBSOLETE_BUILTINS:
        locals()[fname] = disabled_function(fname)
    __all__ = OBSOLETE_BUILTINS
else:
    __all__ = []
