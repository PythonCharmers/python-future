.. _changelog:

What's new
==========

v0.8.1:
  * Backported socketserver.py. Fixes sporadic test failures with http.server
    (related to threading and old-style classes used in Py2.7's
    SocketServer.py).

  * Move a few more safe ``futurize`` fixes from stage2 to stage1

  * Bug fixes to ``future.utils``
  
v0.8:
  * Added Python 2.6 support

  * Removed unused modules: ``future.six`` and ``future.hacks``

  * Removed undocumented functions from ``future.utils``

v0.7:
  * Added a backported Py3-like ``int`` object (inherits from long).

  * Added utility functions for type-checking and docs about
    ``isinstance()`` uses/alternatives.

  * Fixes and stricter type-checking for bytes and str objects

  * Added many more tests for the ``futurize`` script

  * We no longer disable obsolete Py2 builtins by default with ``from
    future.builtins import *``. Use ``from future.builtins.disabled
    import *`` instead.

v0.6:
  * Added a backported Py3-like ``str`` object (inherits from Py2's ``unicode``)

  * Removed support for the deprecated form ``from future import *``: use ``from future.builtins import *`` instead

v0.5.3:
  * Doc improvements

v0.5.2:
  * Add lots of docs and a Sphinx project

v0.5.1:
  * Upgraded included ``six`` module (included as ``future.utils.six``) to v1.4.1

  * ``http.server`` module backported

  * bytes.split() and .rsplit() bugfixes

v0.5.0:
  * Added backported Py3-like ``bytes`` object

v0.4.2:
  * Various fixes

v0.4.1:
  * Added ``open()`` (from ``io`` module on Py2)
  * Improved docs

v0.4.0:
  * Added various useful compatibility functions to ``future.utils``

  * Reorganized package: moved all builtins to ``future.builtins``; moved
    all stdlib things to ``future.standard_library``

  * Renamed ``python-futurize`` console script to ``futurize``

  * Moved ``future.six`` to ``future.utils.six`` and pulled the most relevant
    definitions to ``future.utils``.

  * More improvements to "Py3 to both" conversion (futurize.py --from3)

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

  * New functions added: ``round()``, ``input()``

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
