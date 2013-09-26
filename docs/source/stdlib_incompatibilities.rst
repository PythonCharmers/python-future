.. _stdlib-incompatibilities:

Standard library incompatibilities
==================================

Some standard library interfaces have changed in ways that require
different code than normal Py3 code in order to achieve Py3/2
compatibility.

Here we will attempt to document these, together with known workarounds:

.. csv-table:: Standard library incompatibilities
   :header: "module", "object / feature", "section"
   :widths: 10, 20, 15

   ``array``, ``array`` constructor, :ref:`stdlib-array-constructor`
   ``array``, ``array.read()`` method, :ref:`stdlib-array-read`
   ``base64``, ``decodebytes()`` function, :ref:`stdlib-base64-decodebytes`
   ``re``, ``ASCII`` mode, :ref:`stdlib-re-ASCII`

To contribute to this, please email the python-porting list or send a
pull request. See :ref:`contributing`.


.. _stdlib-array-constructor:

array.array()
-------------

The first argument to ``array.array(typecode[, initializer])`` must be a native
platform string: unicode string on Python 3, byte string on Python 2.

Python 2::
    >>> array.array(b'b')
    array.array(b'b')
    
    >>> array.array(u'u')
    TypeError: must be char, not unicode

Python 3::
    >>> array.array(b'b')
    TypeError: must be a unicode character, not bytes
    
    >>> array.array(u'b')
    array('b')

This means that the typecode cannot be specified portably across Python 3 and Python 2
with a single string literal when ``from __future__ import unicode_literals`` is in effect.

You can use the following code on both Python 3 and Python 2::

    from __future__ import unicode_literals
    from future.utils import bytes_to_native_str
    import array

    # ...
    
    a = array.array(bytes_to_native_str(b'b'))


.. _stdlib-array-read:

array.array.read()
------------------
This method has been removed in Py3. This crops up in e.g. porting ``http.client``.


.. _stdlib-base64-decodebytes:

base64.decodebytes()
--------------------
The ``base64`` module on Py2 has no 'decodebytes'.


.. _stdlib-re-ASCII:

re.ASCII
--------
Python 3 code using regular expressions sometimes looks like this (from
:mod:`urllib.request`)::

    re.compile(r":\d+$", re.ASCII)

This enables 'ASCII mode' for regular expressions (see the docs `here
<http://docs.python.org/3/library/re.html#re.ASCII>`_). Python 2's
:mod:`re` module has no equivalent mode.


