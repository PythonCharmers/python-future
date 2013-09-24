bytes object
============

Handling ``bytes`` consistently and correctly has been one of the most
difficult tasks in writing a Py3/2 compatible codebase. This is because the
Python 2 ``bytes`` object is (unfortunately) simply an alias for Python 2's
``str``, whereas the Python 3 ``bytes`` object is substantially different. For example:

- bytes objects print with a b'' prefix like b'ABCD' on Py3.

- Python 3 often raises TypeErrors to guard against implicit type conversions
  from byte-strings to Unicode.

``future`` contains a backport of the ``bytes`` object from Python 3 which
passes most of the Python 3 tests for ``bytes``. You can use it as follows::

    from future.builtins import bytes
    
    b = bytes(b'ABCD')

This object inherits from Python 2's ``str``, but it enforces the much stricter
separation from unicode strings that Python 3's ``bytes`` requires::

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

The easiest way to ensure identical use of byte-strings compatibly between Python 3 and 2 is to wrap all byte-string literals ``b'...'`` in a ``bytes()`` call, as follows::
    
    from future.builtins import *
    
    # ...

    b = bytes(b'This is my bytestring')

    # ...

