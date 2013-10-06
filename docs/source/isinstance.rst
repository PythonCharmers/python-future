isinstance
----------

``isinstance`` checks are sometimes fragile and generally discouraged in
Python code (in favour of duck typing). Instances of ``isinstance``
require some special handling to achieve portability between Python 3 and
Python 2.

After these imports::
    
    from __future__ import unicode_literals
    from future.builtins import *

The following tests pass on Py3 but fail on Py2::

    >>> s = u'my unicode string'
    >>> assert isinstance(s, str)

    >>> b = b'my byte-string'
    >>> assert isinstance(b, bytes)

    >>> i = 10
    >>> assert isinstance(i, int)

    >>> l = 10**100
    >>> assert isinstance(l, int)

This section describes some preferred cross-platform idioms for
performing such checks and some utility functions in :mod:`future.utils`
that assist with writing clean code.


Distinguishing bytes from unicode text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On Python 2, (unicode) string literals ``'...'`` and byte-string literals
``b'...'`` create instances of the superclasses of the backported
:class:`str` and :class:`bytes` types from :mod:`future.builtins` (i.e.
the native Py2 unicode and 8-bit string types).

If type-checking is necessary to distinguish unicode text from bytes
portably across Py3 and Py2, utility functions called :func:`istext` and
:func:`isbytes` are available in :mod:`future.utils`. You can use them
as follows::

    >>> from __future__ import unicode_literals
    >>> from future.builtins import *
    >>> from future.utils import istext, isbytes

    >>> assert istext('My (unicode) string')
    >>> assert istext(str('My (unicode) string'))

    >>> assert isbytes(b'My byte-string')
    >>> assert isbytes(bytes(b'My byte-string'))

``istext(s)`` tests whether the object ``s`` is (or inherits from) a
unicode string. It is equivalent to the following expression::

    isinstance(s, type(u''))

which is ``True`` if ``s`` is a native Py3 string, Py2 unicode object, or
:class:`future.builtins.str` object on Py2.

Likewise, ``isbytes(b)`` tests whether ``b`` is (or inherits from) an
8-bit byte-string. It is equivalent to::

    isinstance(b, type(b''))

which is ``True`` if ``b`` is a native Py3 bytes object, Py2 8-bit str,
or :class:`future.builtins.bytes` object on Py2.


Integers and long integers
~~~~~~~~~~~~~~~~~~~~~~~~~~

Python 3 unifies Python 2's concepts of integers (``int``) and long
integers (``long``) into a single ``int`` type.

The preferred way to test if a variable is an integer on Py3 or either an
``int`` or ``long`` on Py2 is with the abstract base class :class:`Integral`
from the :mod:`numbers` module as follows::

    >>> from numbers import Integral

    >>> assert isinstance(10, Integral)
    >>> assert isinstance(10**1000, Integral)


Library code
~~~~~~~~~~~~

If you are passing any of the backported types (``bytes``, ``str``,
``int``) into brittle library code where you cannot control ``isinstance``
checks, it may be necessary to upcast the types to their native 
superclasses on Py2. A function ``future.utils.native`` is provided for
this.

Here is how to use it. (The output showing is from Py2)::

    >>> from future.builtins import *
    >>> from future.utils import native

    >>> a = int(10**20)     # long int
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

Here are some real-world examples from the standard library and other
popular libraries::

    TODO: write me!

