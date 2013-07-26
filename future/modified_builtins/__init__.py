"""
This module contains backports of non-essential functionality from Python
3 to Python 2 -- i.e. where there is a simple and perfectly viable
cross-platform way to express the same idea.

For example:
- a Python 2 backport of the range iterator from Py3 with slicing
  support.
- the magic zero-argument super() function

Importing these features is only necessary if the Python 3 code uses
these features and the developers would prefer not to use the
backward-compatible interfaces for some reason.

It is used as follows:

    from __future__ import division, absolute_import, print_function
    from future.features import range, super

And then, for example:

    for i in range(10**11)[:10]:
        pass

and:

    class VerboseList(list):
        def append(self, item):
            print('Adding an item')
            super().append(item)    	# new simpler super() function

range() is a custom class that backports the slicing behaviour from
Python 3 (from the xrange module by Dan Crosta). super() is based on Ryan
Kelly's magicsuper module. See the docstrings for the
``future.features.newsuper`` and ``future.features.newrange`` modules for
more details.

"""

from __future__ import division, absolute_import, print_function

from future import six

if not six.PY3:
    from future.features.newrange import range
    from future.features.newsuper import super
else:
    import builtins
    range = builtins.range
    super = builtins.super

__all__ = ['range', 'super']
