.. _whats-new:

What's New
**********

.. _whats-new-0.15.x:

What's new in version 0.15.2 (2015-09-11)
=========================================

This is a minor bug-fix release:

- Fix ``socket.create_connection()`` backport on Py2.6 (issue #162)
- Add more tests of ``urllib.request`` etc.
- Fix ``newsuper()`` calls from the ``__init__`` method of PyQt subclassses
  (issue #160, thanks to Christopher Arndt)

What's new in version 0.15.1 (2015-09-09)
=========================================

This is a minor bug-fix release:

- Use 3-argument ``socket.create_connection()`` backport to restore Py2.6
  compatibility in ``urllib.request.urlopen()`` (issue #162)
- Remove breakpoint in ``future.backports.http.client`` triggered on certain
  data (issue #164)
- Move ``exec`` fixer to stage 1 of ``futurize`` because the forward-compatible ``exec(a, b)``
  idiom is supported in Python 2.6 and 2.7. See
  https://docs.python.org/2/reference/simple_stmts.html#exec.


What's new in version 0.15.0 (2015-07-25)
=========================================

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

Previous versions
=================

See :ref:`whats-old` for versions prior to v0.15.
