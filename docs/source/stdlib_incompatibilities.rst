.. _stdlib-incompatibilities:
Standard library incompatibilities
==================================

There are sources of incompatibility in the standard library between Python 3 and Python 2.7. Here we will attempt to document these:

.. csv-table:: Standard library incompatibilities
   :header: "module", "object", "Description"
   :widths: 15, 10, 30

   ``array``, ``array`` constructor, :ref:`stdlib-array-constructor`
   ``array``, ``array.read()`` method, :ref:`stdlib-array-read`
   ``base64``, ``decodebytes()`` function, :ref:`base64-decodebytes`



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


.. _stdlib-base64_decodebytes:
base64.decodebytes()
--------------------
The ``base64`` module on Py2 has no 'decodebytes'. [TODO: describe workaround]

