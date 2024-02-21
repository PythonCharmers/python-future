.. _whats-old:

Changes in previous versions
****************************

Changes in the most recent major version are here: :ref:`whats-new`.

Changes in version 0.18.3 (2023-01-13)
======================================
This is a minor bug-fix release containing a number of fixes:

- Backport fix for bpo-38804 (c91d70b)
- Fix bug in fix_print.py fixer (dffc579)
- Fix bug in fix_raise.py fixer (3401099)
- Fix newint bool in py3 (fe645ba)
- Fix bug in super() with metaclasses (6e27aac)
- docs: fix simple typo, reqest -> request (974eb1f)
- Correct __eq__ (c780bf5)
- Pass if lint fails (2abe00d)
- Update docker image and parcel out to constant variable.  Add comment to update version constant (45cf382)
- fix order (f96a219)
- Add flake8 to image (046ff18)
- Make lint.sh executable (58cc984)
- Add docker push to optimize CI (01e8440)
- Build System (42b3025)
- Add docs build status badge to README.md (3f40bd7)
- Use same docs requirements in tox (18ecc5a)
- Add docs/requirements.txt (5f9893f)
- Add PY37_PLUS, PY38_PLUS, and PY39_PLUS (bee0247)
- fix 2.6 test, better comment (ddedcb9)
- fix 2.6 test (3f1ff7e)
- remove nan test (4dbded1)
- include list test values (e3f1a12)
- fix other python2 test issues (c051026)
- fix missing subTest (f006cad)
- import from old imp library on older python versions (fc84fa8)
- replace fstrings with format for python 3.4,3.5 (4a687ea)
- minor style/spelling fixes (8302d8c)
- improve cmp function, add unittest (0d95a40)
- Pin typing==3.7.4.1 for Python 3.3 compatiblity (1a48f1b)
- Fix various py26 unit test failures (9ca5a14)
- Add initial contributing guide with docs build instruction (e55f915)
- Add docs building to tox.ini (3ee9e7f)
- Support NumPy's specialized int types in builtins.round (b4b54f0)
- Added r""" to the docstring to avoid warnings in python3 (5f94572)
- Add __subclasscheck__ for past.types.basestring (c9bc0ff)
- Correct example in README (681e78c)
- Add simple documentation (6c6e3ae)
- Add pre-commit hooks (a9c6a37)
- Handling of __next__ and next by future.utils.get_next was reversed (52b0ff9)
- Add a test for our fix (461d77e)
- Compare headers to correct definition of str (3eaa8fd)
- #322 Add support for negative ndigits in round; additionally, fixing a bug so that it handles passing in Decimal properly (a4911b9)
- Add tkFileDialog to future.movers.tkinter (f6a6549)
- Sort before comparing dicts in TestChainMap (6126997)
- Fix typo (4dfa099)
- Fix formatting in "What's new" (1663dfa)
- Fix typo (4236061)
- Avoid DeprecationWarning caused by invalid escape (e4b7fa1)
- Fixup broken link to external django documentation re: porting to Python 3 and unicode_literals (d87713e)
- Fixed newdict checking version every time (99030ec)
- Add count from 2.7 to 2.6 (1b8ef51)

Changes in version 0.18.2 (2019-10-30)
======================================

This is a minor bug-fix release containing a number of fixes:

- Fix min/max functions with generators, and 'None' default (PR #514)
- Use BaseException in raise_() (PR #515)
- Fix builtins.round() for Decimals (Issue #501)
- Fix raise_from() to prevent failures with immutable classes (PR #518)
- Make FixInput idempotent (Issue #427)
- Fix type in newround (PR #521)
- Support mimetype guessing in urllib2 for Py3.8+ (Issue #508)

Python 3.8 is not yet officially supported.

Changes in version 0.18.1 (2019-10-09)
======================================

This is a minor bug-fix release containing a fix for raise_() 
when passed an exception that's not an Exception (e.g. BaseException
subclasses)

Changes in version 0.18.0 (2019-10-09)
======================================

This is a major bug-fix and feature release, including:

- Fix collections.abc import for py38+
- Remove import for isnewbytes() function, reducing CPU cost significantly
- Fix bug with importing past.translation when importing past which breaks zipped python installations
- Fix an issue with copyreg import under Py3 that results in unexposed stdlib functionality
- Export and document types in future.utils
- Update behavior of newstr.__eq__() to match str.__eq__() as per reference docs
- Fix raising and the raising fixer to handle cases where the syntax is ambiguous
- Allow "default" parameter in min() and max() (Issue #334)
- Implement __hash__() in newstr (Issue #454)
- Future proof some version checks to handle the fact that Py4 won't be a major breaking release
- Fix urllib.request imports for Python 3.8 compatibility (Issue #447)
- Fix future import ordering (Issue #445)
- Fixed bug in fix_division_safe fixture (Issue #434)
- Do not globally destroy re.ASCII in PY3
- Fix a bug in email.Message.set_boundary() (Issue #429)
- Implement format_map() in str
- Implement readinto() for socket.fp

As well as a number of corrections to a variety of documentation, and updates to
test infrastructure.

Changes in version 0.17.1 (2018-10-30)
======================================

This release address a packaging error because of an erroneous declaration that
any built wheels are universal.

Changes in version 0.17.0 (2018-10-19)
======================================

This is a major bug-fix release, including:

- Fix ``from collections import ChainMap`` after install_aliases() (issue #226)
- Fix multiple import from ``__future__`` bug in futurize (issue #113)
- Add support for proper %s formatting of newbytes
- Properly implement iterator protocol for newrange object
- Fix ``past.translation`` on read-only file systems
- Fix Tkinter import bug introduced in Python 2.7.4 (issue #262)
- Correct TypeError to ValueError in a specific edge case for newrange
- Support inequality tests between newstrs and newbytes
- Add type check to __get__ in newsuper
- Fix fix_divsion_safe to support better conversion of complex expressions, and
  skip obvious float division.

As well as a number of corrections to a variety of documentation, and updates to
test infrastructure.

Changes in version 0.16.0 (2016-10-27)
======================================

This release removes the ``configparser`` package as an alias for
``ConfigParser`` on Py2 to improve compatibility with the backported
`configparser package <https://pypi.org/project/configparser/>`. Previously
``python-future`` and the PyPI ``configparser`` backport clashed, causing
various compatibility issues. (Issues #118, #181)

If your code previously relied on ``configparser`` being supplied by
``python-future``, the recommended upgrade path is to run ``pip install
configparser`` or add ``configparser`` to your ``requirements.txt`` file.

Note that, if you are upgrading ``future`` with ``pip``, you may need to
uninstall the old version of future or manually remove the
``site-packages/future-0.15.2-py2.7.egg`` folder for this change to take
effect on your system.

This releases also fixes these bugs:

- Fix ``newbytes`` constructor bug. (Issue #171)
- Fix semantics of ``bool()`` with ``newobject``. (Issue #211)
- Fix ``standard_library.install_aliases()`` on PyPy. (Issue #205)
- Fix assertRaises for ``pow`` and ``compile``` on Python 3.5. (Issue #183)
- Fix return argument of ``future.utils.ensure_new_type`` if conversion to
  new type does not exist. (Issue #185)
- Add missing ``cmp_to_key`` for Py2.6. (Issue #189)
- Allow the ``old_div`` fixer to be disabled. (Issue #190)
- Improve compatibility with Google App Engine. (Issue #231)
- Add some missing imports to the ``tkinter`` and ``tkinter.filedialog``
  package namespaces. (Issues #212 and #233)
- More complete implementation of ``raise_from`` on PY3. (Issues #141,
  #213 and #235, fix provided by Varriount)


Changes in version 0.15.2 (2015-09-11)
======================================

This is a minor bug-fix release:

- Fix ``socket.create_connection()`` backport on Py2.6 (issue #162)
- Add more tests of ``urllib.request`` etc.
- Fix ``newsuper()`` calls from the ``__init__`` method of PyQt subclassses
  (issue #160, thanks to Christopher Arndt)

Changes in version 0.15.1 (2015-09-09)
======================================

This is a minor bug-fix release:

- Use 3-argument ``socket.create_connection()`` backport to restore Py2.6
  compatibility in ``urllib.request.urlopen()`` (issue #162)
- Remove breakpoint in ``future.backports.http.client`` triggered on certain
  data (issue #164)
- Move ``exec`` fixer to stage 1 of ``futurize`` because the forward-compatible ``exec(a, b)``
  idiom is supported in Python 2.6 and 2.7. See
  https://docs.python.org/2/reference/simple_stmts.html#exec.


Changes in version 0.15.0 (2015-07-25)
======================================

This release fixes compatibility bugs with CherryPy's Py2/3 compat layer and
the latest version of the ``urllib3`` package. It also adds some additional
backports for Py2.6 and Py2.7 from Py3.4's standard library.

New features:

- ``install_aliases()`` now exposes full backports of the Py3 urllib submodules
  (``parse``, ``request`` etc.) from ``future.backports.urllib`` as submodules
  of ``urllib`` on Py2.  This implies, for example, that
  ``urllib.parse.unquote`` now takes an optional encoding argument as it does
  on Py3. This improves compatibility with CherryPy's Py2/3 compat layer (issue
  #158).
- ``tkinter.ttk`` support (issue #151)
- Backport of ``collections.ChainMap`` (issue #150)
- Backport of ``itertools.count`` for Py2.6 (issue #152)
- Enable and document support for the ``surrogateescape`` error handler for ``newstr`` and ``newbytes`` objects on Py2.x (issue #116). This feature is currently in alpha.
- Add constants to ``http.client`` such as ``HTTP_PORT`` and ``BAD_REQUEST`` (issue #137)
- Backport of ``reprlib.recursive_repr`` to Py2

Bug fixes:

- Add ``HTTPMessage`` to ``http.client``, which is missing from ``httplib.__all__`` on Python <= 2.7.10. This restores compatibility with the latest ``urllib3`` package (issue #159, thanks to Waldemar Kornewald)
- Expand newint.__divmod__ and newint.__rdivmod__ to fall back to <type 'long'>
  implementations where appropriate (issue #146 - thanks to Matt Bogosian)
- Fix newrange slicing for some slice/range combos (issue #132, thanks to Brad Walker)
- Small doc fixes (thanks to Michael Joseph and Tim Tröndle)
- Improve robustness of test suite against opening .pyc files as text on Py2
- Update backports of ``Counter`` and ``OrderedDict`` to use the newer
  implementations from Py3.4. This fixes ``.copy()`` preserving subclasses etc.
- ``futurize`` no longer breaks working Py2 code by changing ``basestring`` to
  ``str``. Instead it imports the ``basestring`` forward-port from
  ``past.builtins`` (issues #127 and #156)
- ``future.utils``: add ``string_types`` etc. and update docs (issue #126)


.. _whats-new-0.14.x:

Changes in version 0.14.3 (2014-12-15)
======================================

This is a bug-fix release:

- Expose contents of ``thread`` (not ``dummy_thread``) as ``_thread`` on Py2 (Issue #124)
- Add signed support for ``newint.to_bytes()`` (Issue #128)
- Fix ``OrderedDict.clear()`` on Py2.6 (Issue #125)
- Improve ``newrange``: equality and slicing, start/stop/step properties, refactoring (Issues #129, #130)
- Minor doc updates

Changes in version 0.14.2 (2014-11-21)
======================================

This is a bug-fix release:

- Speed up importing of ``past.translation`` (Issue #117)
- ``html.escape()``: replace function with the more robust one from Py3.4
- ``futurize``: avoid displacing encoding comments by ``__future__`` imports (Issues #97, #10, #121)
- ``futurize``: don't swallow exit code (Issue #119)
- Packaging: don't forcibly remove the old build dir in ``setup.py`` (Issue #108)
- Docs: update further docs and tests to refer to ``install_aliases()`` instead of
  ``install_hooks()``
- Docs: fix ``iteritems`` import error in cheat sheet (Issue #120)
- Tests: don't rely on presence of ``test.test_support`` on Py2 or ``test.support`` on Py3 (Issue #109)
- Tests: don't override existing ``PYTHONPATH`` for tests (PR #111)

Changes in version 0.14.1 (2014-10-02)
======================================

This is a minor bug-fix release:

- Docs: add a missing template file for building docs (Issue #108)
- Tests: fix a bug in error handling while reporting failed script runs (Issue #109)
- ``install_aliases()``: don't assume that the ``test.test_support`` module always
  exists on Py2 (Issue #109)


Changes in version 0.14.0 (2014-10-02)
======================================

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

You can now use the following interface for much Python 2/3 compatible code::

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
here: :ref:`direct-imports`.)

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
  (Issue #104)

- This release also removes the broken ``--doctests_only`` option from the ``futurize``
  and ``pasteurize`` scripts for now. (Issue #103)

Internal cleanups
-----------------

The project folder structure has changed. Top-level packages are now in a
``src`` folder and the tests have been moved into a project-level ``tests``
folder.

The following deprecated internal modules have been removed (Issue #80):

- ``future.utils.encoding`` and ``future.utils.six``.

Deprecations
------------

The following internal functions have been deprecated and will be removed in a future release:

- ``future.standard_library.scrub_py2_sys_modules``
- ``future.standard_library.scrub_future_sys_modules``


.. _whats-new-0.13.x:

Changes in version 0.13.1 (2014-09-23)
======================================

This is a bug-fix release:

- Fix (multiple) inheritance of ``future.builtins.object`` with metaclasses (Issues #91, #96)
- Fix ``futurize``'s refactoring of ``urllib`` imports (Issue #94)
- Fix ``futurize --all-imports`` (Issue #101)
- Fix ``futurize --output-dir`` logging (Issue #102)
- Doc formatting fix (Issues #98, #100)


Changes in version 0.13.0 (2014-08-13)
======================================

This is mostly a clean-up release. It adds some small new compatibility features
and fixes several bugs.

Deprecations
------------

The following unused internal modules are now deprecated. They will be removed in a
future release:

- ``future.utils.encoding`` and ``future.utils.six``.

(Issue #80). See `here <http://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries>`_
for the rationale for unbundling them.


New features
------------

- Docs: Add :ref:`compatible-idioms` from Ed Schofield's PyConAU 2014 talk.
- Add ``newint.to_bytes()`` and ``newint.from_bytes()``. (Issue #85)
- Add ``future.utils.raise_from`` as an equivalent to Py3's ``raise ... from
  ...`` syntax. (Issue #86)
- Add ``past.builtins.oct()`` function.
- Add backports for Python 2.6 of ``subprocess.check_output()``,
  ``itertools.combinations_with_replacement()``, and ``functools.cmp_to_key()``.

Bug fixes
---------

- Use a private logger instead of the global logger in
  ``future.standard_library`` (Issue #82). This restores compatibility of the
  standard library hooks with ``flask``. (Issue #79)
- Stage 1 of ``futurize`` no longer renames ``next`` methods to ``__next__``
  (Issue #81). It still converts ``obj.next()`` method calls to
  ``next(obj)`` correctly.
- Prevent introduction of a second set of parentheses in ``print()`` calls in
  some further cases.
- Fix ``isinstance`` checks for subclasses of future types. (Issue #89)
- Be explicit about encoding file contents as UTF-8 in unit tests. (Issue #63)
  Useful for building RPMs and in other environments where ``LANG=C``.
- Fix for 3-argument ``pow(x, y, z)`` with ``newint`` arguments. (Thanks to @str4d.)
  (Issue #87)


.. _whats-new-0.12.4:

Changes in version 0.12.4 (2014-07-18)
======================================

- Fix upcasting behaviour of ``newint``. (Issue #76)


.. _whats-new-0.12.3:

Changes in version 0.12.3 (2014-06-19)
======================================

- Add "official Python 3.4 support": Py3.4 is now listed among the PyPI Trove
  classifiers and the tests now run successfully on Py3.4. (Issue #67)

- Add backports of ``collections.OrderedDict`` and
  ``collections.Counter`` for Python 2.6. (Issue #52)

- Add ``--version`` option for ``futurize`` and ``pasteurize`` scripts.
  (Issue #57)

- Fix ``future.utils.ensure_new_type`` with ``long`` input. (Issue #65)

- Remove some false alarms on checks for ambiguous fixer names with
  ``futurize -f ...``.

- Testing fixes:
    - Don't hard-code Python interpreter command in tests. (Issue #62)
    - Fix deprecated ``unittest`` usage in Py3. (Issue #62)
    - Be explicit about encoding temporary file contents as UTF-8 for
      when ``LANG=C`` (e.g., when building an RPM). (Issue #63)
    - All undecorated tests are now passing again on Python 2.6, 2.7, 3.3,
      and 3.4 (thanks to Elliott Sales de Andrade).

- Docs:
    - Add list of fixers used by ``futurize``. (Issue #58)
    - Add list of contributors to the Credits page.

.. _whats-new-0.12.2:

Changes in version 0.12.2 (2014-05-25)
======================================

- Add ``bytes.maketrans()`` method. (Issue #51)
- Add support for Python versions between 2.7.0 and 2.7.3 (inclusive).
  (Issue #53)
- Bug fix for ``newlist(newlist([1, 2, 3]))``. (Issue #50)


.. _whats-new-0.12.1:

Changes in version 0.12.1 (2014-05-14)
======================================

- Python 2.6 support: ``future.standard_library`` now isolates the ``importlib``
  dependency to one function (``import_``) so the ``importlib`` backport may
  not be needed.

- Doc updates


.. _whats-new-0.12:

Changes in version 0.12.0 (2014-05-06)
======================================

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
``future.builtins.object``) that can streamline Py2/3 compatible code by
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
Issue #37). This includes new ``execfile()`` and ``cmp()`` functions.
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

There is no corresponding ``listkeys(d)`` function; use ``list(d)`` instead.


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

Or with this new interface::

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

Instead of::

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
  displaced by ``from __future__ import ...`` statements. (Issue #10)

- Improved compatibility with ``py2exe`` (`Issue #31 <https://github.com/PythonCharmers/python-future/issues/31>`_).

- The ``future.utils.bytes_to_native_str`` function now returns a platform-native string
  object and ``future.utils.native_str_to_bytes`` returns a ``newbytes`` object on Py2.
  (`Issue #47 <https://github.com/PythonCharmers/python-future/issues/47>`_).

- The backported ``http.client`` module and related modules use other new
  backported modules such as ``email``. As a result they are more compliant
  with the Python 3.3 equivalents.


.. _whats-new-0.11.4:

Changes in version 0.11.4 (2014-05-25)
======================================

This release contains various small improvements and fixes:

- This release restores Python 2.6 compatibility. (Issue #42)

- The ``fix_absolute_import`` fixer now supports Cython ``.pyx`` modules. (Issue
  #35)

- Right-division with ``newint`` objects is fixed. (Issue #38)

- The ``fix_dict`` fixer has been moved to stage2 of ``futurize``.

- Calls to ``bytes(string, encoding[, errors])`` now work with ``encoding`` and
  ``errors`` passed as positional arguments. Previously this only worked if
  ``encoding`` and ``errors`` were passed as keyword arguments.


- The 0-argument ``super()`` function now works from inside static methods such
  as ``__new__``. (Issue #36)

- ``future.utils.native(d)`` calls now work for ``future.builtins.dict`` objects.


.. _whats-new-0.11.3:

Changes in version 0.11.3 (2014-02-27)
======================================

This release has improvements in the standard library import hooks mechanism and
its compatibility with 3rd-party modules:


Improved compatibility with ``requests``
----------------------------------------

The ``__exit__`` function of the ``hooks`` context manager and the
``remove_hooks`` function both now remove submodules of
``future.standard_library`` from the ``sys.modules`` cache. Therefore this code
is now possible on Python 2 and 3::

       from future import standard_library
       standard_library.install_hooks()
       import http.client
       standard_library.remove_hooks()
       import requests

       data = requests.get('http://www.google.com')


Previously, this required manually removing ``http`` and ``http.client`` from
``sys.modules`` before importing ``requests`` on Python 2.x. (Issue #19)

This change should also improve the compatibility of the standard library hooks
with any other module that provides its own Python 2/3 compatibility code.

Note that the situation will improve further in version 0.12; import hooks will
require an explicit function call or the ``hooks`` context manager.


Conversion scripts explicitly install import hooks
--------------------------------------------------

The ``futurize`` and ``pasteurize`` scripts now add an explicit call to
``install_hooks()`` to install the standard library import hooks. These scripts
now add these two lines::

       from future import standard_library
       standard_library.install_hooks()

instead of just the first one. The next major version of ``future`` (0.12) will
require the explicit call or use of the ``hooks`` context manager. This will
allow finer-grained control over whether import hooks are enabled for other
imported modules, such as ``requests``, which provide their own Python 2/3
compatibility code.


``futurize`` script no longer adds ``unicode_literals`` by default
------------------------------------------------------------------

There is a new ``--unicode-literals`` flag to ``futurize`` that adds the
import::

    from __future__ import unicode_literals

to the top of each converted module. Without this flag, ``futurize`` now no
longer adds this import. (Issue #22)

The ``pasteurize`` script for converting from Py3 to Py2/3 still adds
``unicode_literals``. (See the comments in Issue #22 for an explanation.)


.. _whats-new-0.11:

Changes in version 0.11 (2014-01-28)
====================================

There are several major new features in version 0.11.


``past`` package
----------------

The python-future project now provides a ``past`` package in addition to the
``future`` package. Whereas ``future`` provides improved compatibility with
Python 3 code to Python 2, ``past`` provides support for using and interacting
with Python 2 code from Python 3. The structure reflects that of ``future``,
with ``past.builtins`` and ``past.utils``. There is also a new
``past.translation`` package that provides transparent translation of Python 2
code to Python 3. (See below.)

One purpose of ``past`` is to ease module-by-module upgrades to
codebases from Python 2. Another is to help with enabling Python 2 libraries to
support Python 3 without breaking the API they currently provide. (For example,
user code may expect these libraries to pass them Python 2's 8-bit strings,
rather than Python 3's ``bytes`` object.) A third purpose is to help migrate
projects to Python 3 even if one or more dependencies are still on Python 2.

Currently ``past.builtins`` provides forward-ports of Python 2's ``str`` and
``dict`` objects, ``basestring``, and list-producing iterator functions.  In
later releases, ``past.builtins`` will be used internally by the
``past.translation`` package to help with importing and using old Python 2
modules in a Python 3 environment.


Auto-translation of Python 2 modules upon import
------------------------------------------------

``past`` provides an experimental ``translation`` package to help
with importing and using old Python 2 modules in a Python 3 environment.

This is implemented using import hooks that attempt to automatically
translate Python 2 modules to Python 3 syntax and semantics upon import. Use
it like this::

    $ pip3 install plotrique==0.2.5-7 --no-compile   # to ignore SyntaxErrors
    $ python3

Then pass in a whitelist of module name prefixes to the
``past.translation.autotranslate()`` function. Example::

    >>> from past.translation import autotranslate
    >>> autotranslate(['plotrique'])
    >>> import plotrique


This is intended to help you migrate to Python 3 without the need for all
your code's dependencies to support Python 3 yet. It should be used as a
last resort; ideally Python 2-only dependencies should be ported
properly to a Python 2/3 compatible codebase using a tool like
``futurize`` and the changes should be pushed to the upstream project.

For more information, see :ref:`translation`.


Separate ``pasteurize`` script
------------------------------

The functionality from ``futurize --from3`` is now in a separate script called
``pasteurize``. Use ``pasteurize`` when converting from Python 3 code to Python
2/3 compatible source. For more information, see :ref:`backwards-conversion`.


``pow()``
---------

There is now a ``pow()`` function in ``future.builtins.misc`` that behaves like
the Python 3 ``pow()`` function when raising a negative number to a fractional
power (returning a complex number).


``input()`` no longer disabled globally on Py2
----------------------------------------------

Previous versions of ``future`` deleted the ``input()`` function from
``__builtin__`` on Python 2 as a security measure. This was because
Python 2's ``input()`` function allows arbitrary code execution and could
present a security vulnerability on Python 2 if someone expects Python 3
semantics but forgets to import ``input`` from ``future.builtins``. This
behaviour has been reverted, in the interests of broadening the
compatibility of ``future`` with other Python 2 modules.

Please remember to import ``input`` from ``future.builtins`` if you use
``input()`` in a Python 2/3 compatible codebase.


.. _deprecated-auto-import-hooks:

Deprecated feature: auto-installation of standard-library import hooks
----------------------------------------------------------------------

Previous versions of ``python-future`` installed import hooks automatically upon
importing the ``standard_library`` module from ``future``. This has been
deprecated in order to improve robustness and compatibility with modules like
``requests`` that already perform their own single-source Python 2/3
compatibility.

As of v0.12, importing ``future.standard_library``
will no longer install import hooks by default. Instead, please install the
import hooks explicitly as follows::

    from future import standard_library
    standard_library.install_hooks()

And uninstall them after your import statements using::

    standard_library.remove_hooks()

*Note*: This is a backward-incompatible change.



Internal changes
----------------

The internal ``future.builtins.backports`` module has been renamed to
``future.builtins.types``. This will change the ``repr`` of ``future``
types but not their use.


.. _whats-new-0.10.2:

Changes in version 0.10.2 (2014-01-11)
======================================

New context-manager interface to ``standard_library.hooks``
-----------------------------------------------------------

There is a new context manager ``future.standard_library.hooks``. Use it like
this::

    from future import standard_library
    with standard_library.hooks():
        import queue
        import configserver
        from http.client import HTTPConnection
        # etc.

If not using this context manager, it is now encouraged to add an explicit call to
``standard_library.install_hooks()`` as follows::

    from future import standard_library
    standard_library.install_hooks()

    import queue
    import html
    import http.client
    # etc.

And to remove the hooks afterwards with::

    standard_library.remove_hooks()

The functions ``install_hooks()`` and ``remove_hooks()`` were previously
called ``enable_hooks()`` and ``disable_hooks()``. The old names are
deprecated (but are still available as aliases).

As usual, this feature has no effect on Python 3.


.. _whats-new-0.10:

Changes in version 0.10.0 (2013-12-02)
======================================

Backported ``dict`` type
------------------------

``future.builtins`` now provides a Python 2 ``dict`` subclass whose
:func:`keys`, :func:`values`, and :func:`items` methods produce
memory-efficient iterators. On Python 2.7, these also have the same set-like
view behaviour as on Python 3. This can streamline code needing to iterate
over large dictionaries. For example::

    from __future__ import print_function
    from future.builtins import dict, range

    squares = dict({i: i**2 for i in range(10**7)})

    assert not isinstance(d.items(), list)
    # Because items() is memory-efficient, so is this:
    square_roots = dict((i_squared, i) for (i, i_squared) in squares.items())

For more information, see :ref:`dict-object`.


Utility functions ``raise_`` and ``exec_``
------------------------------------------

The functions ``raise_with_traceback()`` and ``raise_()`` were
added to ``future.utils`` to offer either the Python 3.x or Python 2.x
behaviour for raising exceptions. Thanks to Joel Tratner for the
contribution of these. ``future.utils.reraise()`` is now deprecated.

A portable ``exec_()`` function has been added to ``future.utils`` from
``six``.


Bugfixes
--------
- Fixed ``newint.__divmod__``
- Improved robustness of installing and removing import hooks in :mod:`future.standard_library`
- v0.10.1: Fixed broken ``pip install future`` on Py3


.. _whats-new-0.9:

Changes in version 0.9 (2013-11-06)
===================================


``isinstance`` checks are supported natively with backported types
------------------------------------------------------------------

The ``isinstance`` function is no longer redefined in ``future.builtins``
to operate with the backported ``int``, ``bytes`` and ``str``.
``isinstance`` checks with the backported types now work correctly by
default; we achieve this through overriding the ``__instancecheck__``
method of metaclasses of the backported types.

For more information, see :ref:`isinstance-calls`.


``futurize``: minimal imports by default
----------------------------------------

By default, the ``futurize`` script now only adds the minimal set of
imports deemed necessary.

There is now an ``--all-imports`` option to the ``futurize`` script which
gives the previous behaviour, which is to add all ``__future__`` imports
and ``from future.builtins import *`` imports to every module. (This even
applies to an empty ``__init__.py`` file.)


Looser type-checking for the backported ``str`` object
------------------------------------------------------

Now the ``future.builtins.str`` object behaves more like the Python 2
``unicode`` object with regard to type-checking. This is to work around some
bugs / sloppiness in the Python 2 standard library involving mixing of
byte-strings and unicode strings, such as ``os.path.join`` in ``posixpath.py``.

``future.builtins.str`` still raises the expected ``TypeError`` exceptions from
Python 3 when attempting to mix it with ``future.builtins.bytes``.


``suspend_hooks()`` context manager added to ``future.standard_library``
------------------------------------------------------------------------

Pychecker (as of v0.6.1)'s ``checker.py`` attempts to import the ``builtins``
module as a way of determining whether Python 3 is running. Since this
succeeds when ``from future import standard_library`` is in effect, this
check does not work and pychecker sets the wrong value for its internal ``PY2``
flag is set.

To work around this, ``future`` now provides a context manager called
``suspend_hooks`` that can be used as follows::

    from future import standard_library
    ...
    with standard_library.suspend_hooks():
        from pychecker.checker import Checker


.. _whats-new-0.8:

Changes in version 0.8 (2013-10-28)
===================================

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


``isinstance()`` added to :mod:`future.builtins` (v0.8.2)
---------------------------------------------------------

It is now possible to use ``isinstance()`` calls normally after importing ``isinstance`` from
``future.builtins``. On Python 2, this is specially defined to be compatible with
``future``'s backported ``int``, ``str``, and ``bytes`` types, as well as
handling Python 2's ``int``/``long`` distinction.

The result is that code that uses ``isinstance`` to perform type-checking of
ints, strings, and bytes should now work identically on Python 2 as on Python 3.

The utility functions ``isint``, ``istext``, and ``isbytes`` provided before for
compatible type-checking across Python 2 and 3 in :mod:`future.utils` are now
deprecated.


.. _changelog:

Summary of all changes
======================

v0.15.0:
  * Full backports of ``urllib.parse`` and other ``urllib`` submodules are exposed by ``install_aliases()``.
  * ``tkinter.ttk`` support
  * Initial ``surrogateescape`` support
  * Additional backports: ``collections``, ``http`` constants, etc.
  * Bug fixes

v0.14.3:
  * Bug fixes

v0.14.2:
  * Bug fixes

v0.14.1:
  * Bug fixes

v0.14.0:
  * New top-level ``builtins`` package on Py2 for cleaner imports. Equivalent to
    ``future.builtins``
  * New top-level packages on Py2 with the same names as Py3 standard modules:
    ``configparser``, ``copyreg``, ``html``, ``http``, ``xmlrpc``, ``winreg``

v0.13.1:
  * Bug fixes

v0.13.0:
  * Cheat sheet for writing Python 2/3 compatible code
  * ``to_int`` and ``from_int`` methods for ``newbytes``
  * Bug fixes

v0.12.0:
  * Add ``newobject`` and ``newlist`` types
  * Improve compatibility of import hooks with ``Requests``, ``py2exe``
  * No more auto-installation of import hooks by ``future.standard_library``
  * New ``future.moves`` package
  * ``past.builtins`` improved
  * ``newstr.encode(..., errors='surrogateescape')`` supported
  * Refactoring: ``future.standard_library`` submodules -> ``future.backports``
  * Refactoring: ``future.builtins.types`` -> ``future.types``
  * Refactoring: ``past.builtins.types`` -> ``past.types``
  * New ``listvalues`` and ``listitems`` functions in ``future.utils``
  * Many bug fixes to ``futurize``, ``future.builtins``, etc.

v0.11.4:
  * Restore Py2.6 compatibility

v0.11.3:
  * The ``futurize`` and ``pasteurize`` scripts add an explicit call to
    ``future.standard_library.install_hooks()`` whenever modules affected by
    PEP 3108 are imported.

  * The ``future.builtins.bytes`` constructor now accepts ``frozenset``
    objects as on Py3.

v0.11.2:
  * The ``past.translation.autotranslate`` feature now finds modules to import
    more robustly and works with Python eggs.

v0.11.1:
  * Update to ``requirements_py26.txt`` for Python 2.6. Small updates to
    docs and tests.

v0.11:
  * New ``past`` package with ``past.builtins`` and ``past.translation``
    modules.

v0.10.2:
  * Improvements to stdlib hooks. New context manager:
    ``future.standard_library.hooks()``.

  * New ``raise_`` and ``raise_with_traceback`` functions in ``future.utils``.

v0.10:
  * New backported ``dict`` object with set-like ``keys``, ``values``, ``items``

v0.9:
  * :func:`isinstance` hack removed in favour of ``__instancecheck__`` on the
    metaclasses of the backported types
  * ``futurize`` now only adds necessary imports by default
  * Looser type-checking by ``future.builtins.str`` when combining with Py2
    native byte-strings.

v0.8.3:
  * New ``--all-imports`` option to ``futurize``
  * Fix bug with ``str.encode()`` with encoding as a non-keyword arg

v0.8.2:
  * New ``isinstance`` function in :mod:`future.builtins`. This obviates
    and deprecates the utility functions for type-checking in :mod:`future.utils`.

v0.8.1:
  * Backported ``socketserver.py``. Fixes sporadic test failures with
    ``http.server`` (related to threading and old-style classes used in Py2.7's
    ``SocketServer.py``).

  * Move a few more safe ``futurize`` fixes from stage2 to stage1

  * Bug fixes to :mod:`future.utils`

v0.8:
  * Added Python 2.6 support

  * Removed unused modules: :mod:`future.six` and :mod:`future.hacks`

  * Removed undocumented functions from :mod:`future.utils`

v0.7:
  * Added a backported Py3-like ``int`` object (inherits from ``long``).

  * Added utility functions for type-checking and docs about
    ``isinstance`` uses/alternatives.

  * Fixes and stricter type-checking for ``bytes`` and ``str`` objects

  * Added many more tests for the ``futurize`` script

  * We no longer disable obsolete Py2 builtins by default with ``from
    future.builtins import *``. Use ``from future.builtins.disabled
    import *`` instead.

v0.6:
  * Added a backported Py3-like ``str`` object (inherits from Py2's ``unicode``)

  * Removed support for the form ``from future import *``; use ``from future.builtins import *`` instead

v0.5.3:
  * Doc improvements

v0.5.2:
  * Add lots of docs and a Sphinx project

v0.5.1:
  * Upgraded included ``six`` module (included as ``future.utils.six``) to v1.4.1

  * :mod:`http.server` module backported

  * ``bytes.split()`` and ``.rsplit()`` bugfixes

v0.5.0:
  * Added backported Py3-like ``bytes`` object

v0.4.2:
  * Various fixes

v0.4.1:
  * Added :func:`open` (from :mod:`io` module on Py2)
  * Improved docs

v0.4.0:
  * Added various useful compatibility functions to :mod:`future.utils`

  * Reorganized package: moved all builtins to :mod:`future.builtins`; moved
    all stdlib things to ``future.standard_library``

  * Renamed ``python-futurize`` console script to ``futurize``

  * Moved ``future.six`` to ``future.utils.six`` and pulled the most relevant
    definitions to :mod:`future.utils`.

  * More improvements to "Py3 to both" conversion (``futurize.py --from3``)

v0.3.5:
  * Fixed broken package setup ("package directory 'libfuturize/tests' does not exist")

v0.3.4:
  * Added ``itertools.zip_longest``

  * Updated ``2to3_backcompat`` tests to use ``futurize.py``

  * Improved ``libfuturize`` fixers: correct order of imports; add imports only when necessary (except ``absolute_import`` currently)

v0.3.3:
  * Added ``python-futurize`` console script

  * Added ``itertools.filterfalse``

  * Removed docs about unfinished backports (``urllib`` etc.)

  * Removed old Py2 syntax in some files that breaks py3 ``setup.py install``

v0.3.2:
  * Added ``test.support`` module

  * Added ``UserList``, ``UserString``, ``UserDict`` classes to ``collections`` module

  * Removed ``int`` -> ``long`` mapping

  * Added backported ``_markupbase.py`` etc. with new-style classes to fix travis-ci build problems

  * Added working ``html`` and ``http.client`` backported modules
v0.3.0:
  * Generalized import hooks to allow dotted imports

  * Added backports of ``urllib``, ``html``, ``http`` modules from Py3.3 stdlib using ``future``

  * Added ``futurize`` script for automatically turning Py2 or Py3 modules into
    cross-platform Py3 modules

  * Renamed ``future.standard_library_renames`` to
    ``future.standard_library``. (No longer just renames, but backports too.)

v0.2.2.1:
  * Small bug fixes to get tests passing on travis-ci.org

v0.2.1:
  * Small bug fixes

v0.2.0:
  * ``Features`` module renamed to ``modified_builtins``

  * New functions added: :func:`round`, :func:`input`

  * No more namespace pollution as a policy::

        from future import *

    should have no effect on Python 3. On Python 2, it only shadows the
    builtins; it doesn't introduce any new names.

  * End-to-end tests with Python 2 code and ``2to3`` now work

v0.1.0:
  * first version with tests!

  * removed the inspect-module magic

v0.0.x:
  * initial releases. Use at your peril.
