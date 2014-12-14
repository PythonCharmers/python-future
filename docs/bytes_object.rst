.. _bytes-object:

bytes
-----

Handling ``bytes`` consistently and correctly has traditionally been one
of the most difficult tasks in writing a Py2/3 compatible codebase. This
is because the Python 2 :class:`bytes` object is simply an alias for
Python 2's :class:`str`, rather than a true implementation of the Python
3 :class:`bytes` object, which is substantially different.

:mod:`future` contains a backport of the :mod:`bytes` object from Python 3
which passes most of the Python 3 tests for :mod:`bytes`. (See
``tests/test_future/test_bytes.py`` in the source tree.) You can use it as
follows::

    >>> from builtins import bytes
    >>> b = bytes(b'ABCD')

On Py3, this is simply the builtin :class:`bytes` object. On Py2, this
object is a subclass of Python 2's :class:`str` that enforces the same
strict separation of unicode strings and byte strings as Python 3's
:class:`bytes` object::

    >>> b + u'EFGH'      # TypeError
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: argument can't be unicode string
    
    >>> bytes(b',').join([u'Fred', u'Bill'])
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: sequence item 0: expected bytes, found unicode string

    >>> b == u'ABCD'
    False

    >>> b < u'abc'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unorderable types: bytes() and <type 'unicode'>


In most other ways, these :class:`bytes` objects have identical
behaviours to Python 3's :class:`bytes`::

    b = bytes(b'ABCD')
    assert list(b) == [65, 66, 67, 68]
    assert repr(b) == "b'ABCD'"
    assert b.split(b'B') == [b'A', b'CD']

Currently the easiest way to ensure identical behaviour of byte-strings
in a Py2/3 codebase is to wrap all byte-string literals ``b'...'`` in a
:func:`~bytes` call as follows::
    
    from builtins import bytes
    
    # ...

    b = bytes(b'This is my bytestring')

    # ...

This is not perfect, but it is superior to manually debugging and fixing
code incompatibilities caused by the many differences between Py3 bytes
and Py2 strings.


..
    .. _bytes-test-results:
    
    bytes test results
    ~~~~~~~~~~~~~~~~~~
    
    For reference, when using Py2's default :class:`bytes` (i.e.
    :class:`str`), running the ``bytes`` unit tests from Python 3.3's
    ``test_bytes.py`` on Py2 (after fixing imports) gives this::
    
        --------------------------------------------------------------
        Ran 203 tests in 0.209s
        
        FAILED (failures=31, errors=55, skipped=1)
        --------------------------------------------------------------
    
    Using :mod:`future`'s backported :class:`bytes` object passes most of
    the same Python 3.3 tests on Py2, except those requiring specific
    wording in exception messages.
    
    See ``future/tests/test_bytes.py`` in the source for the actual set
    of unit tests that are actually run.

