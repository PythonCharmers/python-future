.. _isinstance-calls:

isinstance
----------

The following tests all pass on Python 3::
    
    >>> assert isinstance(2**62, int)
    >>> assert isinstance(2**63, int)
    >>> assert isinstance(b'my byte-string', bytes)
    >>> assert isinstance(u'unicode string 1', str)
    >>> assert isinstance('unicode string 2', str)


However, two normally fail on Python 2::

    >>> assert isinstance(2**63, int)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AssertionError

    >>> assert isinstance(u'my unicode string', str)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AssertionError

And if this import is in effect on Python 2::

    >>> from __future__ import unicode_literals

then the fifth test fails too::

    >>> assert isinstance('unicode string 2', str)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AssertionError


After importing the builtins from ``future``, the tests pass on Python 2 as
on Python 3::

    >>> from __future__ import unicode_literals
    >>> from future.builtins import *

    >>> assert isinstance(10, int)
    >>> assert isinstance(10**100, int)
    >>> assert isinstance(b'my byte-string', bytes)
    >>> assert isinstance(u'unicode string 1', str)
    >>> assert isinstance('unicode string 2', str)

Note that the last test requires that ``unicode_literals`` be imported to succeed.


Passing data to/from Python 2 libraries
---------------------------------------

If you are passing any of the backported types (``bytes``, ``str``,
``int``) into brittle library code that performs type-checks using ``type()``,
rather than ``isinstance()``, or requires that you pass Python 2's native types
(rather than subclasses) for some other reason, it may be necessary to upcast
the types from ``future`` to their native superclasses on Py2. A function
``future.utils.native`` is provided for this.

Here is how to use it. (The output showing is from Py2)::

    >>> from future.builtins import *
    >>> from future.utils import native

    >>> a = int(10**20)     # Py3-like long int
    >>> a
    100000000000000000000
    >>> type(a)
    future.builtins.backports.newint.newint
    >>> native(a)
    100000000000000000000L
    >>> type(native(a))
    long
    
    >>> b = bytes(b'ABC')
    >>> type(b)
    future.builtins.backports.newbytes.newbytes
    >>> native(b)
    'ABC'
    >>> type(native(b))
    str
    
    >>> s = str(u'ABC')
    >>> type(s)
    future.builtins.backports.newstr.newstr
    >>> native(s)
    u'ABC'
    >>> type(native(s))
    unicode

On Py3, the :func:`native` function is a no-op.


Native string type
------------------

Some library code, include standard library code like the ``array.array()``
constructor, require native strings on Python 2 and Python 3. This means that
there is no simple way to pass the appropriate string type when the
``unicode_literals`` import from ``__future__`` is in effect.

The objects ``native_str`` and ``native_bytes`` are available in 
``future.utils`` for this case. These are equivalent to ``__builtin__.str`` on
Python 2 or ``builtins.str`` on Python 3.

Alternatively, the functions ``native_str_to_bytes`` and
``bytes_to_native_str`` are also available for conversions.


.. ``isinstance`` checks are sometimes fragile and generally discouraged in
.. Python code (in favour of duck typing). When passing ``future``'s backported
.. ``int``, ``str``, or ``bytes`` types from Python 3 to standard library code
.. or 3rd-party modules on Python 2 that contain checks with ``isinstance``, some 
.. special handling may be required to achieve portability.
.. 
.. This section explains the issues involved and describes some utility functions
.. in :mod:`future.utils` that assist with writing clean code.
.. 
.. Distinguishing bytes from unicode text
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. 
.. On Python 2, (unicode) string literals ``'...'`` and byte-string literals
.. ``b'...'`` create instances of the superclasses of the backported
.. :class:`str` and :class:`bytes` types from :mod:`future.builtins` (i.e.
.. the native Py2 unicode and 8-bit string types). Therefore ``isinstance`` checks
.. in standard library code or 3rd-party modules should succeed. Just keep in mind
.. that with ``future``, ``str`` and ``bytes`` are like Python 3's types of the
.. same names.

.. Old
.. ~~~
.. If type-checking is necessary to distinguish unicode text from bytes
.. portably across Py3 and Py2, utility functions called :func:`istext` and
.. :func:`isbytes` are available in :mod:`future.utils`. You can use them
.. as follows::
.. 
..     >>> from __future__ import unicode_literals
..     >>> from future.builtins import *
..     >>> from future.utils import istext, isbytes
.. 
..     >>> assert istext('My (unicode) string')
..     >>> assert istext(str('My (unicode) string'))
.. 
..     >>> assert isbytes(b'My byte-string')
..     >>> assert isbytes(bytes(b'My byte-string'))
.. 
.. ``istext(s)`` tests whether the object ``s`` is (or inherits from) a
.. unicode string. It is equivalent to the following expression::
.. 
..     isinstance(s, type(u''))
.. 
.. which is ``True`` if ``s`` is a native Py3 string, Py2 unicode object, or
.. :class:`future.builtins.str` object on Py2.
.. 
.. Likewise, ``isbytes(b)`` tests whether ``b`` is (or inherits from) an
.. 8-bit byte-string. It is equivalent to::
.. 
..     isinstance(b, type(b''))
.. 
.. which is ``True`` if ``b`` is a native Py3 bytes object, Py2 8-bit str,
.. or :class:`future.builtins.bytes` object on Py2.


.. Integers and long integers
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~
.. 
.. Python 3 unifies Python 2's concepts of integers (``int``) and long
.. integers (``long``) into a single ``int`` type.
.. 
.. On Python 2, checks such as ``isinstance(x, int)`` are fragile because
.. ``long`` does not inherit from ``int``. So when an integer gets too
.. large, the check starts to fail. For example::
.. 
..     >>> x = 2**62
..     >>> assert isinstance(x, int)
..     >>> x *= 2
..     >>> assert isinstance(x, int)
..     Traceback (most recent call last):
..       File "<stdin>", line 1, in <module>
..     AssertionError
.. 
.. ``future``'s backported ``int`` object doesn't help with these checks;
.. both of them fail. To test if a variable is an integer on Py3 or either an
.. ``int`` or ``long`` on Py2, you can use the ``future.utils.isint``
..  function::
.. 
..     >>> from future.utils import isint
.. 
..     >>> assert isint(10)
..     >>> assert isint(10**1000)
.. 
.. An alternative is to use the abstract base class :class:`Integral`
.. from the :mod:`numbers` module as follows::
.. 
..     >>> from numbers import Integral
.. 
..     >>> assert isinstance(10, Integral)
..     >>> assert isinstance(10**1000, Integral)



