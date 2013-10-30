.. _whats-new:

What's new in version 0.8
=========================

Python 2.6 support
------------------

``future`` now includes support for Python 2.6.

To run the ``future`` test suite on Python 2.6, this additional package is needed::

    pip install unittest2

``http.server`` also requires the ``argparse`` package::

    pip install argparse


Unused modules removed
----------------------

The ``future.six`` module has been removed. ``future`` doesn't require ``six``
(and hasn't since version 0.3). If you need support for Python versions before
2.6, ``six`` is the best option. ``future`` and ``six`` can be installed
alongside each other easily if needed.

The unused ``hacks`` module has also been removed from the source tree.


isinstance() added to :mod:`future.builtins` (v0.8.2)
-----------------------------------------------------

It is now possible to use ``isinstance()`` calls normally after importing ``isinstance`` from 
``future.builtins``. On Python 2, this is specially defined to be compatible with
``future``'s backported ``int``, ``str``, and ``bytes`` types, as well as
handling Python 2's int/long distinction.

The result is that code that uses ``isinstance`` to perform type-checking of
ints, strings, and bytes should now work identically on Python 2 as on Python 3.

The utility functions ``isint``, ``istext``, and ``isbytes`` provided before for
compatible type-checking across Python 2 and 3 in :mod:`future.utils` are now
deprecated.

