What's New in v0.12.x
*********************


.. whats-new-0.12.2:

What's new in version 0.12.2
============================

- Add ``bytes.maketrans()`` method (issue #51)
- Add support for Python versions between 2.7.0 and 2.7.3 (inclusive). (Patch
  contributed by Nicolas Delaby.) (issue #53)
- Bug fix for ``newlist(newlist([1, 2, 3]))``: issue #50


.. whats-new-0.12.1:

What's new in version 0.12.1
============================

- Python 2.6 support: ``future.standard_library`` now isolates the ``importlib``
  dependency to one function (``import_``) so the ``importlib`` backport may
  not be needed.

- Doc updates


.. whats-new-0.12:

What's new in version 0.12.0
============================

The major new feature in this version is improvements in the support for the
reorganized standard library (PEP 3108) and compatibility of the import
mechanism with 3rd-party modules.

More robust standard-library import hooks
-----------------------------------------

**Note: backwards-incompatible change:** As previously announced (see
:ref:`deprecated-auto-import-hooks`), the import hooks must now be enabled
explicitly, as follows::

    from future import standard_library
    with standard_library.hooks():
        import html.parser
        import http.client
        ...

This now causes these modules to be imported from ``future.moves``, a new
package that provides wrappers over the native Python 2 standard library with
the new Python 3 organization. As a consequence, the import hooks provided in
``future.standard_library`` are now fully compatible with the `Requests library
<http://python-requests.org>`_.

The functional interface with ``install_hooks()`` is still supported for
backwards compatibility::

    from future import standard_library
    standard_library.install_hooks():

    import html.parser
    import http.client
    ...
    standard_library.remove_hooks()

Explicit installation of import hooks allows finer-grained control
over whether they are enabled for other imported modules that provide their own
Python 2/3 compatibility layer. This also improves compatibility of ``future``
with tools like ``py2exe``.


``newobject`` base object defines fallback Py2-compatible special methods
-------------------------------------------------------------------------

There is a new ``future.types.newobject`` base class (available as
``future.builtins.object``) that can streamline Py3/2 compatible code by
providing fallback Py2-compatible special methods for its subclasses. It
currently provides ``next()`` and ``__nonzero__()`` as fallback methods on Py2
when its subclasses define the corresponding Py3-style ``__next__()`` and
``__bool__()`` methods.

This obviates the need to add certain compatibility hacks or decorators to the
code such as the ``@implements_iterator`` decorator for classes that define a
Py3-style ``__next__`` method.

In this example, the code defines a Py3-style iterator with a ``__next__``
method. The ``object`` class defines a ``next`` method for Python 2 that maps
to ``__next__``::
    
    from future.builtins import object

    class Upper(object):
        def __init__(self, iterable):
            self._iter = iter(iterable)
        def __next__(self):                 # note the Py3 interface
            return next(self._iter).upper()
        def __iter__(self):
            return self

    assert list(Upper('hello')) == list('HELLO')

``newobject`` defines other Py2-compatible special methods similarly:
currently these include ``__nonzero__`` (mapped to ``__bool__``) and
``__long__`` (mapped to ``__int__``).

Inheriting from ``newobject`` on Python 2 is safe even if your class defines
its own Python 2-style ``__nonzero__`` and ``next`` and ``__long__`` methods.
Your custom methods will simply override those on the base class.

On Python 3, as usual, ``future.builtins.object`` simply refers to ``builtins.object``.


``past.builtins`` module improved
---------------------------------

The ``past.builtins`` module is much more compatible with the corresponding
builtins on Python 2; many more of the Py2 unit tests pass on Py3. For example,
functions like ``map()`` and ``filter()`` now behave as they do on Py2 with with
``None`` as the first argument.

The ``past.builtins`` module has also been extended to add Py3 support for
additional Py2 constructs that are not adequately handled by ``lib2to3`` (see
issue #37). This includes new ``execfile()`` and ``cmp()`` functions.
``futurize`` now invokes imports of these functions from ``past.builtins``.


``surrogateescape`` error handler
---------------------------------

The ``newstr`` type (``future.builtins.str``) now supports a backport of the
Py3.x ``'surrogateescape'`` error handler for preserving high-bit
characters when encoding and decoding strings with unknown encodings.


``newlist`` type
----------------

There is a new ``list`` type in ``future.builtins`` that offers ``.copy()`` and
``.clear()`` methods like the ``list`` type in Python 3.


``listvalues`` and ``listitems``
--------------------------------

``future.utils`` now contains helper functions ``listvalues`` and
``listitems``, which provide Python 2-style list snapshotting semantics for
dictionaries in both Python 2 and Python 3.

These came out of the discussion around Nick Coghlan's now-withdrawn PEP 469.

There is no corresponding ``listkeys(d)`` function. Use ``list(d)`` for this case.


Tests
-----

The number of unit tests has increased from 600 to over 800. Most of the new
tests come from Python 3.3's test suite.


Refactoring of ``future.standard_library.*`` -> ``future.backports``
--------------------------------------------------------------------

The backported standard library modules have been moved to ``future.backports``
to make the distinction clearer between these and the new ``future.moves``
package.


Backported ``http.server`` and ``urllib`` modules
-------------------------------------------------

Alpha versions of backports of the ``http.server`` and ``urllib`` module from
Python 3.3's standard library are now provided in ``future.backports``.

Use them like this::

    from future.backports.urllib.request import Request    # etc.
    from future.backports.http import server as http_server

or with this new interface::

    from future.standard_library import import_, from_import

    Request = from_import('urllib.request', 'Request', backport=True)
    http = import_('http.server', backport=True)

..    from future.standard_library.email import message_from_bytes  # etc.
..    from future.standard_library.xmlrpc import client, server


Internal refactoring
--------------------

The ``future.builtins.types`` module has been moved to ``future.types``.
Likewise, ``past.builtins.types`` has been moved to ``past.types``. The only
user-visible effect of this is to change ``repr(type(obj))`` for instances
of these types. For example::

    >>> from future.builtins import bytes
    >>> bytes(b'abc')
    >>> type(b)
    future.types.newbytes.newbytes

instead of::

    >>> type(b)           # prior to v0.12
    future.builtins.types.newbytes.newbytes


Bug fixes
---------

Many small improvements and fixes have been made across the project. Some highlights are:

- Fixes and updates from Python 3.3.5 have been included in the backported
  standard library modules.

- Scrubbing of the ``sys.modules`` cache performed by ``remove_hooks()`` (also
  called by the ``suspend_hooks`` and ``hooks`` context managers) is now more
  conservative.
  
..  Is this still true?
..  It now removes only modules with Py3 names (such as
..  ``urllib.parse``) and not the corresponding ``future.standard_library.*``
..  modules (such as ``future.standard_library.urllib.parse``.

- The ``fix_next`` and ``fix_reduce`` fixers have been moved to stage 1 of
  ``futurize``.

- ``futurize``: Shebang lines such as ``#!/usr/bin/env python`` and source code
  file encoding declarations like ``# -*- coding=utf-8 -*-`` are no longer occasionally
  displaced by ``from __future__ import ...`` statements. (Issue #10.)

- Improved compatibility with py2exe (`issue #31 <https://github.com/PythonCharmers/python-future/issues/31>`_).

- The ``future.utils.bytes_to_native_str`` function now returns a platform-native string
  object and ``future.utils.native_str_to_bytes`` returns a ``newbytes`` object on Py2.
  (`Issue #47 <https://github.com/PythonCharmers/python-future/issues/47>`_).

- The backported ``http.client`` module and related modules use other new
  backported modules such as ``email``. As a result they are more compliant
  with the Python 3.3 equivalents.

