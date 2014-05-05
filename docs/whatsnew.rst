What's new
**********


.. whats-new-0.12:

What's new in version 0.12
==========================

The major new feature in this version is improvements in the support for the
reorganized standard library (PEP 3108) and compatibility of the import
mechanism with 3rd-party modules.

Standard-library import hooks now require explicit installation
---------------------------------------------------------------

*Note: backwards-incompatible change:* As previously announced (see
:ref:`deprecated-auto-import-hooks`), the import hooks must now be enabled
explicitly, as follows::

    from future import standard_library
    with standard_library.hooks():
        import html.parser
        import http.client
        ...

This now causes these modules to be imported from ``future.moves``, a new
package that provides wrappers over the native Python 2 standard library with
the new Python 3 organization.

The functional interface is now deprecated but still supported for backwards
compatibility::

    from future import standard_library
    standard_library.install_hooks():

    import html.parser
    import http.client
    ...
    standard_library.remove_hooks()

This allows finer-grained control over whether import hooks are enabled for
other imported modules, such as ``requests``, which provide their own Python
2/3 compatibility code. This also improves compatibility of ``future`` with
tools like ``py2exe``.


.. Versioned standard library imports
.. ----------------------------------
.. 
.. ``future`` now offers a choice of either backported versions of the standard library modules from Python 3.3 or renamed Python 2.7 versions. Use it as follows::
.. 
..     from future import standard_library
..     standard_library.install_hooks(version='3.3')
..     import html.parser
..     ...
..     standard_library.remove_hooks()
.. 
.. or as follows::
..     
..     from future import standard_library
..     with standard_library.hooks(version='2.7'):
..         import html.parser
..         ...
.. 
.. If ``version='2.7'`` is selected, on Python 2.7 the import hooks provide an interface to the
.. Python 2.7 standard library modules remapped to their equivalent Python 3.x names. For example, the above code is equivalent to this on Python 2.7 (more or less)::
.. 
..     import htmllib
..     module = type(htmllib)
..     html = module('html')
..     html.parser = module('html.parser')
..     html.parser.HTMLParser = htmllib.HTMLParser
..     html.parser.HTMLParseError = htmllib.htmlParseError
.. 
.. but the dozen or so other functions in Python 3.3's ``html.parser`` module are not available on Python 2.7.
.. 
.. 
.. If ``version=='3.3'`` is selected, 
.. 
.. These are not (yet) full backports of
.. the Python 3.3
.. modules but remappings to the corresponding
.. functionality in the Python 2.x standard library.


``newobject`` base object defines fallback Py2-compatible special methods
-------------------------------------------------------------------------

There is a new ``future.builtins.object`` base class that can streamline Py3/2
compatible code by providing fallback Py2-compatible special methods for its
subclasses. It currently provides ``next()`` and ``__nonzero__()`` as fallback
methods on Py2 when its subclasses define the corresponding Py3-style
``__next__()`` and ``__bool__()`` methods.

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

``future.builtins.object`` defines other Py2-compatible special methods similarly:
currently these include ``__nonzero__`` (mapped to ``__bool__``) and
``__long__`` (mapped to ``__int__``).

Inheriting from ``newobject`` on Python 2 is safe even if your class defines
its own Python 2-style ``__nonzero__`` and ``next`` and ``__long__`` methods.
Your custom methods will simply override those on the base class.

On Python 3, as usual, ``object`` simply refers to ``builtins.object``.


``past.builtins`` module improved
---------------------------------

The ``past.builtins`` module is much more compatible with the corresponding
builtins on Python 2; many more of the Py2 unit tests pass on Py3. For example,
functions like ``map()`` and ``filter()`` now behave as they do on Py2 with with
``None`` as the first argument.

The ``past.builtins`` module has also been extended to add Py3 support for
additional Py2 constructs that are not adequately handled by ``lib2to3`` (see
issue #37). This includes custom ``execfile()`` and ``cmp()`` functions.
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
  displaced by ``from __future__ import ...`` statements.

- Improved compatibility with py2exe (`issue #31 <https://github.com/PythonCharmers/python-future/issues/31>`_).

- The ``future.utils.bytes_to_native_str`` function now returns a ``native_str``
  object and ``future.utils.native_str_to_bytes`` returns a ``newbytes`` on Py2.
  (`Issue #47 <https://github.com/PythonCharmers/python-future/issues/47>`_).

- The backported ``http.client`` module and related modules use other new
  backported modules such as ``email``. As a result they are more compliant
  with the Python 3.3 equivalents.


.. whats-new-0.11.5:

.. What's new in version 0.11.5
.. ============================
.. 
.. This is a minor bugfix release contains small improvements to way the standard
.. library hook interact with the ``sys.modules`` cache.


.. whats-new-0.11.4:

What's new in version 0.11.4
============================

This release contains various small improvements and fixes:

- This release restores Python 2.6 compatibility. (Issue #42).

- The ``fix_absolute_import`` fixer now supports Cython ``.pyx`` modules. (Issue
  #35).

- Right-division with ``newint`` objects is fixed. (Issue #38).

- The ``fix_dict`` fixer has been moved to stage2 of ``futurize``.

- Calls to ``bytes(string, encoding[, errors])`` now work with ``encoding`` and
  ``errors`` passed as positional arguments. Previously this only worked if
  ``encoding`` and ``errors`` were passed as keyword arguments.


- The 0-argument ``super()`` function now works from inside static methods such
  as ``__new__``. (Issue #36).

- ``future.utils.native(d)`` calls now work for ``future.builtins.dict`` objects.


.. whats-new-0.11.3:

What's new in version 0.11.3
============================

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
``sys.modules`` before importing ``requests`` on Python 2.x. (Issue #19).
   
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
longer adds this import. (Issue #22).

The ``pasteurize`` script for converting from Py3 to Py2/3 still adds
``unicode_literals``. (See the comments in issue #22 for an explanation.)


.. whats-new-0.11:

What's new in version 0.11
==========================

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
    
Then pass in a whitelist of module name prefixes to the ``past.autotranslate()``
function. Example::
    
    >>> from past import autotranslate
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


pow()
-----

There is now a ``pow()`` function in ``future.builtins.misc`` that behaves like
the Python 3 ``pow()`` function when raising a negative number to a fractional
power (returning a complex number).


input() no longer disabled globally on Py2
------------------------------------------

Previous versions of ``future`` deleted the ``input()`` function from
``__builtin__`` on Python 2 as a security measure. This was because
Python 2's ``input()`` function allows arbitrary code execution and could
present a security vulnerability on Python 2 if someone expects Python 3
semantics but forgets to import ``input`` from ``future.builtins``. This
behaviour has been reverted, in the interests of broadening the
compatibility of ``future`` with other Python 2 modules.

Please remember to import ``input`` from ``future.builtins`` if you use
``input()`` in a Python 2/3 compatible codebase.


.. deprecated-auto-import-hooks

Deprecated feature: auto-installation of standard-library import hooks
----------------------------------------------------------------------

Previous versions of ``python-future`` installed import hooks automatically upon
``from future import standard_library``. This has been deprecated in order to
improve robustness and compatibility with modules like ``requests`` that already
perform their own single-source Python 2/3 compatibility.

.. (Previously, the import hooks were
.. bleeding into surrounding code, causing incompatibilities with modules like
.. ``requests`` (issue #19). 

In the next version of ``python-future``, importing ``future.standard_library``
will no longer install import hooks by default. Instead, please install the
import hooks explicitly as follows::
    
    from future import standard_library
    standard_library.install_hooks()

and uninstall them after your import statements using::

    standard_library.remove_hooks()

..  For more fine-grained use of import hooks, the names can be passed explicitly as
..  follows::
.. 
..      from future import standard_library
..      standard_library.install_hooks()


*Note*: this will be a backward-incompatible change.

.. This feature may be resurrected in a later version if a safe implementation can be found.


Internal changes
----------------

The internal ``future.builtins.backports`` module has been renamed to
``future.builtins.types``. This will change the ``repr`` of ``future``
types but not their use.


.. whats-new-0.10.2:

What's new in version 0.10.2
============================


.. Simpler imports
.. ---------------
.. 
.. It is now possible to import builtins directly from the ``future``
.. namespace as follows::
.. 
..     >>> from future import *
..     
.. or just those you need::
.. 
..     >>> from future import open, str


Utility functions for raising exceptions with a traceback portably
------------------------------------------------------------------

The functions ``raise_with_traceback()`` and ``raise_`` were added to
``future.utils`` to offer either the Python 3.x or Python 2.x behaviour
for raising exceptions. Thanks to Joel Tratner for the contribution of
these.


.. whats-new-0.10:

What's new in version 0.10
==========================

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


Refactoring of standard_library hooks (v0.10.2)
-----------------------------------------------

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

and to remove the hooks afterwards with::

    standard_library.remove_hooks()

The functions ``install_hooks()`` and ``remove_hooks()`` were previously
called ``enable_hooks()`` and ``disable_hooks()``. The old names are
still available as aliases, but are deprecated.

As usual, this feature has no effect on Python 3.



Utility functions raise_ and exec_
----------------------------------

The functions ``raise_with_traceback()`` and ``raise_()`` were
added to ``future.utils`` to offer either the Python 3.x or Python 2.x
behaviour for raising exceptions. Thanks to Joel Tratner for the
contribution of these. ``future.utils.reraise()`` is now deprecated.

A portable ``exec_()`` function has been added to ``future.utils`` from
``six``.


Bugfixes
--------
- Fixed newint.__divmod__
- Improved robustness of installing and removing import hooks in :mod:`future.standard_library`
- v0.10.1: Fixed broken ``pip install future`` on Py3


.. whats-new-0.9:

What's new in version 0.9
=========================


``isinstance`` checks supported natively with backported types
--------------------------------------------------------------

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
applies to an empty ``__init__.py`` file.


Looser type-checking for the backported ``str`` object
------------------------------------------------------

Now the ``future.builtins.str`` object behaves more like the Python 2
``unicode`` object with regard to type-checking. This is to work around some
bugs / sloppiness in the Python 2 standard library involving mixing of
byte-strings and unicode strings, such as ``os.path.join`` in ``posixpath.py``.

``future.builtins.str`` still raises the expected ``TypeError`` exceptions from
Python 3 when attempting to mix it with ``future.builtins.bytes``.


suspend_hooks() context manager added to ``future.standard_library``
--------------------------------------------------------------------

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


.. whats-new-0.8:

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


.. changelog:

Summary of all changes
======================

What's new in version 0.11.x
============================

v0.11.4:
  * Restore Py2.6 compatibility

v0.11.3:
  * The ``futurize`` and ``pasteurize`` scripts add an explicit call to
  ``future.standard_library.install_hooks()`` whenever modules affected by PEP
  3108 are imported.

  * The ``future.builtins.bytes`` constructor now accepts ``frozenset``
  objects as on Py3.

v0.11.2:
  * The ``past.autotranslate`` feature now finds modules to import more
  robustly and works with Python eggs.

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
  * Added a backported Py3-like ``int`` object (inherits from long).

  * Added utility functions for type-checking and docs about
    ``isinstance`` uses/alternatives.

  * Fixes and stricter type-checking for bytes and str objects

  * Added many more tests for the ``futurize`` script

  * We no longer disable obsolete Py2 builtins by default with ``from
    future.builtins import *``. Use ``from future.builtins.disabled
    import *`` instead.

v0.6:
  * Added a backported Py3-like ``str`` object (inherits from Py2's ``unicode``)

  * Removed support for the form ``from future import *``: use ``from future.builtins import *`` instead

v0.5.3:
  * Doc improvements

v0.5.2:
  * Add lots of docs and a Sphinx project

v0.5.1:
  * Upgraded included ``six`` module (included as ``future.utils.six``) to v1.4.1

  * :mod:`http.server` module backported

  * bytes.split() and .rsplit() bugfixes

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

  * Updated 2to3_backcompat tests to use futurize.py

  * Improved libfuturize fixers: correct order of imports; add imports only when necessary (except absolute_import currently)

v0.3.3:
  * Added ``python-futurize`` console script

  * Added ``itertools.filterfalse``

  * Removed docs about unfinished backports (urllib etc.)

  * Removed old Py2 syntax in some files that breaks py3 setup.py install

v0.3.2:
  * Added test.support module

  * Added UserList, UserString, UserDict classes to collections module

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
  * Features module renamed to modified_builtins

  * New functions added: :func:`round`, :func:`input`

  * No more namespace pollution as a policy::

        from future import *

    should have no effect on Python 3. On Python 2, it only shadows the
    builtins; it doesn't introduce any new names.

  * End-to-end tests with Python 2 code and 2to3 now work

v0.1.0:
  * first version with tests!

  * removed the inspect-module magic

v0.0.x:
  * initial releases. Use at your peril.
