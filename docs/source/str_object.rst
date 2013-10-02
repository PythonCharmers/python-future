.. _str-object:

str
-----

The :class:`str` object in Python 3 is quite similar but not identical to the
Python 2 :class:`unicode` object. The major differences are:

- repr of unicode strings in Py2 is "u'...'" versus "'...'"
- stricter type-checking in Py3 to enforce the distinction between unicode
  strings and byte-strings, such as when comparing, concatenating, joining, or
  replacing parts of strings.

``future`` contains a backport of the :mod:`str` object from Python 3 which
inherits from the Python 2 :class:`unicode` class but has customizations to
improve compatibility with Python 3's :class:`str` object. You can use it as
follows::

    >>> from __future__ import unicode_literals
    >>> from future.builtins import str

Then, for example::

    >>> s = str(u'ABCD')
    >>> assert s != b'ABCD'
    >>> assert isinstance(s.encode('utf-8'), bytes)
    >>> assert isinstance(b.decode('utf-8'), str)

    These raise TypeErrors:

    >>> b'B' in s
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'in <string>' requires string as left operand, not <type 'str'>

    >>> s.find(b'A')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: argument can't be <type 'str'>

In most other ways, these :class:`str` objects have identical
behaviours to Python 3's :class:`str`::

    >>> s = str('ABCD')
    >>> assert repr(s) == 'ABCD'      # consistent repr with Py3 (no u prefix)
    >>> assert list(s) == ['A', 'B', 'C', 'D']
    >>> assert s.split('B') == ['A', 'CD']

Currently the easiest way to ensure identical use of strings in a Py3/2
codebase is to wrap string literals in a :func:`~str` call, as follows::
    
    from __future__ import unicode_literals
    from future.builtins import *
    
    # ...

    s = str('This absolutely must behave like a Py3 string')

    # ...

Most of the time this is unnecessary, but the stricter type-checking of the
``future.builtins.str`` object, in particular, may be useful while ensuring
that Py2's unicode strings are not mixed up with implicit coercions from
byte-strings.

