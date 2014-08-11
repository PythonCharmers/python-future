.. whats-new-0.13

What's New in v0.13.0
*********************

Deprecations
------------

The following internal modules are deprecated. They will be removed in the next
major release:

- ``future.utils.encoding`` and ``future.utils.six``.

See `here <http://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries`_ for a rationale for unbundling them.

.. - The duplicated ``with_metaclass`` and ``native`` functions and the PY2,
..   PYPY, PY3 constants in the ``past.utils`` module are now deprecated. Use the
..   corresponding functions and constants in ``future.utils`` instead.
..   ``past.utils`` will be removed by Python-Future version 1.0 unless some other  need for it arises by then.

New features
------------

- ``%`` string interpolation with ``bytes`` objects (PEP 461, to be added in
  Python 3.5) is now supported on Python versions 3.3 and 3.4 via a
  ``newbytes`` type.

- Docs: Add :ref:`compatible-idioms` from Ed Schofield's PyConAU 2014 talk.
- Add ``past.builtins.oct()``
- Add ``newint.to_bytes()`` and ``newint.from_bytes()`` (issue #85)
- Add ``future.utils.raise_from`` as an equivalent to Py3's ``raise ... from
  ...`` syntax (issue #86).
- Python 2.6: backport ``subprocess.check_output()``,
  ``itertools.combinations_with_replacement``, and ``functools.cmp_to_key``.
- ``futurize``: now uses a ``--safe`` mode by default which adds some
  extra function calls that guarantee correctness at the expense of producing
  idiomatic Python 3 code. The behaviour in previous versions is equivalent to
  a new mode that can be enabled with ``futurize --aggressive``.

  Currently the only such function call applied is ``past.builtins.div()`` for
  Python 2-style division.

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

Test fixes
----------
- Be explicit about encoding file contents as UTF-8 in unit tests (issue #63). Useful for RPMs and other environments where LANG=C.
- 


