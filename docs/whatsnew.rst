.. _whats-new:

What's New
**********

.. _whats-new-0.14.x:

What's new in version 0.14.3
============================

This is a bug-fix release:

- Expose contents of ``thread`` (not ``dummy_thread``) as ``_thread`` on Py2 (issue #124)
- Add signed support for ``newint.to_bytes()`` (issue #128)
- Fix ``OrderedDict.clear()`` on Py2.6 (issue #125)
- Improve ``newrange``: equality and slicing, start/stop/step properties, refactoring (issues #129, #130)
- Minor doc updates

What's new in version 0.14.2
============================

This is a bug-fix release:

- Speed up importing of ``past.translation`` (issue #117)
- ``html.escape()``: replace function with the more robust one from Py3.4
- futurize: avoid displacing encoding comments by __future__ imports (issues #97, #10, #121)
- futurize: don't swallow exit code (issue #119)
- Packaging: don't forcibly remove the old build dir in ``setup.py`` (issue #108)
- Docs: update further docs and tests to refer to ``install_aliases()`` instead of
  ``install_hooks()``
- Docs: fix ``iteritems`` import error in cheat sheet (issue #120)
- Tests: don't rely on presence of ``test.test_support`` on Py2 or ``test.support`` on Py3 (issue #109)
- Tests: don't override existing ``PYTHONPATH`` for tests (PR #111)

What's new in version 0.14.1
============================

This is a minor bug-fix release:

- Docs: add a missing template file for building docs (issue #108)
- Tests: fix a bug in error handling while reporting failed script runs (issue #109)
- install_aliases(): don't assume that the ``test.test_support`` module always
  exists on Py2 (issue #109)


What's new in version 0.14
==========================

This is a major new release that offers a cleaner interface for most imports in
Python 2/3 compatible code.

Instead of this interface::

    >>> from future.builtins import str, open, range, dict

    >>> from future.standard_library import hooks
    >>> with hooks():
    ...     import queue
    ...     import configparser
    ...     import tkinter.dialog
    ...     # etc.

you can now use the following interface for much Python 2/3 compatible code::

    >>> # Alias for future.builtins on Py2:
    >>> from builtins import str, open, range, dict

    >>> # Alias for future.moves.* on Py2:
    >>> import queue
    >>> import configparser
    >>> import tkinter.dialog
    >>> etc.

Notice that the above code will run on Python 3 even without the presence of the
``future`` package. Of the 44 standard library modules that were refactored with
PEP 3108, 30 are supported with direct imports in this manner. (These are listed
here: :ref:`list-standard-library-renamed`.)

The other 14 standard library modules that kept the same top-level names in
Py3.x are not supported with this direct import interface on Py2. These include
the 5 modules in the Py3 ``urllib`` package. These modules are accessible through
the following interface (as well as the interfaces offered in previous versions
of ``python-future``)::

    from future.standard_library import install_aliases
    install_aliases()

    from collections import UserDict, UserList, UserString
    import dbm.gnu
    from itertools import filterfalse, zip_longest
    from subprocess import getoutput, getstatusoutput
    from sys import intern
    import test.support
    from urllib.request import urlopen
    from urllib.parse import urlparse
    # etc.
    from collections import Counter, OrderedDict     # backported to Py2.6

The complete list of packages supported with this interface is here:
:ref:`list-standard-library-refactored`.

For more information on these and other interfaces to the standard library, see
:ref:`standard-library-imports`.

Bug fixes
---------

- This release expands the ``future.moves`` package to include most of the remaining
  modules that were moved in the standard library reorganization (PEP 3108).
  (Issue #104). See :ref:`list-standard-library-renamed` for an updated list.

- This release also removes the broken ``--doctests_only`` option from the ``futurize``
  and ``pasteurize`` scripts for now (issue #103).

Internal cleanups
-----------------

The project folder structure has changed. Top-level packages are now in a
``src`` folder and the tests have been moved into a project-level ``tests``
folder.

The following deprecated internal modules have been removed (issue #80):

- ``future.utils.encoding`` and ``future.utils.six``.

Deprecations
------------

The following internal functions have been deprecated and will be removed in a future release:

- ``future.standard_library.scrub_py2_sys_modules``
- ``future.standard_library.scrub_future_sys_modules``


Previous versions
=================

See :ref:`whats-old` for versions prior to v0.14.
