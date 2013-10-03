Distinguishing bytes from unicode text
--------------------------------------

After these imports::
    
    from __future__ import unicode_literals
    from future.builtins import *

the following tests pass on Py3 but fail on Py2::

    >>> s = 'my unicode string'
    >>> assert isinstance(s, str)

    >>> b = b'my byte-string'
    >>> assert isinstance(b, bytes)

This is a corner case that results on Py2 with :func:`isinstance` because
(unicode) string literals ``'...'`` and byte-string literals ``b'...'``
create instances of the superclasses of the backported :class:`str` and
:class:`bytes` types from :mod:`future.builtins` (i.e. the native Py2
unicode and 8-bit string types).

If type-checking is necessary to distinguish unicode text from bytes
portably across Py3 and Py2, utility functions called :func:`is_text` and
:func:`is_bytes` are available in :mod:`future.utils`. You can use them
as follows::

    >>> from __future__ import unicode_literals
    >>> from future.builtins import *
    >>> from future.utils import is_text, is_bytes

    >>> assert is_text('My (unicode) string')
    >>> assert is_text(str('My (unicode) string'))

    >>> assert is_bytes(b'My byte-string')
    >>> assert is_bytes(bytes(b'My byte-string'))

``is_text(s)`` tests whether the object ``s`` is (or inherits from) a
unicode string. It is equivalent to the following expression::

    isinstance(s, type(u''))

which is ``True`` if ``s`` is a native Py3 string, Py2 unicode object, or
:class:`future.builtins.str` object on Py2.

Likewise, ``is_bytes(b)`` tests whether ``b`` is (or inherits from) an
8-bit byte-string. It is equivalent to::

    isinstance(b, type(b''))

which is ``True`` if ``b`` is a native Py3 bytes object, Py2 8-bit str,
or :class:`future.builtins.bytes` object on Py2.

