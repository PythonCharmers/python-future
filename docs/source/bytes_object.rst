.. _bytes-object:

bytes
-----

Handling ``bytes`` consistently and correctly has traditionally been one of the
most difficult tasks in writing a Py3/2 compatible codebase. This is because
the Python 2 ``bytes`` object is simply an alias for Python 2's ``str``, rather
than a true implementation of the Python 3 ``bytes`` object, which is
substantially different.

``future`` contains a backport of the ``bytes`` object from Python 3 which
passes most of the Python 3 tests for ``bytes``. (See
:ref:`bytes-test-results`.) You can use it as follows::

    from future.builtins import bytes
    
    b = bytes(b'ABCD')

On Py2, this object inherits from Python 2's native ``str``, but it enforces
the much stricter separation from unicode strings that Python 3's ``bytes``
requires::

    >>> b + u'EFGH'      # TypeError
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: argument can't be unicode string
    
    >>> bytes(b',').join([u'Fred', u'Bill'])
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: sequence item 0: expected bytes, found unicode string

In most other ways, these ``bytes`` objects have identical behaviours to Python 3's ``bytes``::

    b = bytes(b'ABCD')
    assert list(b) == [65, 66, 67, 68]
    assert repr(b) == "b'ABCD'"
    assert b.split(b'b') == [b'A', b'CD']

Currently the easiest way to ensure identical use of byte-strings compatibly between
Python 3 and 2 is to wrap all byte-string literals ``b'...'`` in a ``bytes()``
call, as follows::
    
    from future.builtins import *
    
    # ...

    b = bytes(b'This is my bytestring')

    # ...

This is not perfect, but it is superior to manually debugging and fixing code
incompatibilities caused by the many differences between Py3 bytes and Py2
strings.


.. _bytes-test-results:

Test results
~~~~~~~~~~~~

For reference, when not using the backported ``bytes`` object, running the Py3.3
``bytes`` unit tests in ``test_bytes.py`` on Py2 (after fixing imports) gives
this::

    --------------------------------------------------------------
    Ran 203 tests in 0.209s
    
    FAILED (failures=31, errors=55, skipped=1)
    --------------------------------------------------------------

The ``future`` backport of the Py3 ``bytes`` object passes most of the Python 3
tests for ``bytes`` on Py2, except those requiring specific wording in exception
messages.

See ``future/tests/test_bytes.py`` in the source for the unit tests that are
actually run.

