.. _whats-new-0.13.x:

What's New
**********

What's new in version 0.13.2
============================

- This release expands the ``future.moves`` package to include most of the remaining
  modules that were moved in the standard library reorganization (PEP 3108).
  (Issue #104). See :ref:`list-standard-library-moves` for an updated list.

- This release also removes the broken ``--doctests_only`` option from the ``futurize``
  and ``pasteurize`` scripts for now (issue #103).

What's new in version 0.13.1
============================

This is a bug-fix release:

- Fix (multiple) inheritance of ``future.builtins.object`` with metaclasses (issues #91 and #96)
- Fix ``futurize``'s refactoring of ``urllib`` imports (issue #94)
- Fix ``futurize --all-imports`` (issue #101)
- Fix ``futurize --output-dir`` logging (issue #102)
- Doc formatting fix (issues #98, 100)


What's new in version 0.13
==========================

This is mostly a clean-up release. It adds some small new compatibility features
and fixes several bugs.

Deprecations
------------

The following internal modules are now deprecated. They will be removed in a
future release:

- ``future.utils.encoding`` and ``future.utils.six``.

(Issue #80). See `here <http://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries>`_
for the rationale for unbundling them.


New features
------------

- Docs: Add :ref:`compatible-idioms` from Ed Schofield's PyConAU 2014 talk.
- Add ``newint.to_bytes()`` and ``newint.from_bytes()`` (issue #85)
- Add ``future.utils.raise_from`` as an equivalent to Py3's ``raise ... from
  ...`` syntax (issue #86).
- Add ``past.builtins.oct()`` function.
- Add backports for Python 2.6 of ``subprocess.check_output()``,
  ``itertools.combinations_with_replacement()``, and ``functools.cmp_to_key()``.

Bug fixes
---------

- Use a private logger instead of the global logger in
  ``future.standard_library`` (issue #82).
- Stage 1 of ``futurize`` no longer renames ``next`` methods to ``__next__``
  (issue #81). It still converts ``obj.next()`` method calls to
  ``next(obj)`` correctly.
- Prevent introduction of a second set of parentheses in ``print()`` calls in
  some further cases.
- Fix isinstance checks for subclasses of future types (issue #89).
- Be explicit about encoding file contents as UTF-8 in unit tests (issue #63).
  Useful for building RPMs and in other environments where ``LANG=C``.
- Fix for 3-argument ``pow(x, y, z)`` with ``newint`` arguments (issue #87).
  (Thanks to @str4d).


Previous versions
=================

See the :ref:`whats-old` for versions prior to v0.13.
