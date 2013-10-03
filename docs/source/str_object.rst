.. _str-object:

str
-----

The :class:`str` object in Python 3 is quite similar but not identical to the
Python 2 :class:`unicode` object.

The major difference is the stricter type-checking with Py3 ``str`` to enforce
the distinction between unicode strings and byte-strings, such as when
comparing, concatenating, joining, or replacing parts of strings.

There are also minor differences, such as the ``repr`` of unicode strings in
Py2 having a ``"u'...'"`` prefix, versus simply ``"'...'"``, and the removal of
the :func:`str.decode` method in Py3.

``future`` contains a backport of the :mod:`str` object from Python 3 which
inherits from the Python 2 :class:`unicode` class but has customizations to
improve compatibility with Python 3's :class:`str` object. You can use it as
follows::

    >>> from __future__ import unicode_literals
    >>> from future.builtins import str

(On Py3, this simply imports the builtin :class:`str` object.)

Then, for example, the following code has the same effect on Py2 as on Py3::

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

In most other ways, these :class:`str` objects on Py2 have the same
behaviours as Python 3's :class:`str`::

    >>> s = str('ABCD')
    >>> assert repr(s) == 'ABCD'      # consistent repr with Py3 (no u prefix)
    >>> assert list(s) == ['A', 'B', 'C', 'D']
    >>> assert s.split('B') == ['A', 'CD']

Currently the easiest way to ensure identical use of (unicode) strings across
Py3 and Py2 in a single-source codebase is to wrap string literals in a
:func:`~str` call, as follows::
    
    from __future__ import unicode_literals
    from future.builtins import *
    
    # ...

    s = str('This absolutely must behave like a Py3 string')

    # ...

Most of the time this is unnecessary, but the stricter type-checking of the
``future.builtins.str`` object is useful for ensuring the same consistent
separation between unicode and byte strings on Py2 as on Py3. This is
important when writing protocol handlers, for example.

