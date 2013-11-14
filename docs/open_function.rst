.. _open-function:

open()
------

The Python 3 builtin :func:`open` function for opening files returns file
contents as (unicode) strings unless the binary (``b``) flag is passed, as in::
    
    open(filename, 'rb')

in which case it returns a Py3 :class:`bytes` object.

``future.builtins`` provides a compatible ``open`` function on Py2,
which uses the ``open`` backport available in the standard library :mod:`io`
module on Py2.6+.

When porting code from Python 2, be aware of the different return types from
methods such as :func:`read()` from the file object that ``open`` returns.

Note that the output of :func:`read()` etc. is not automatically cast to the
appropriate ``future.builtins.bytes`` or ``future.builtins.str`` type. If you
need the stricter type-checking of Py3 on Py2 as well, you can cast it
explicitly as follows::

    from __future__ import unicode_literals
    from future.builtins import *

    data = open('image.png', 'rb').read()
    # On Py2, data is a standard 8-bit str with loose Unicode coercion.
    # data + u'' would likely raise a UnicodeDecodeError

    data = bytes(data)
    # Now it behaves like a Py3 bytes object...

    assert data[:4] == b'\x89PNG'
    assert data[4] == 13     # integer
    # Raises TypeError:
    # data + u''

