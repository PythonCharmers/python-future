Python 3/2 Single-Source Compatibility Reference
================================================

This document details what is required to achieve compatibility between Python
3 and Python 2.7 in a single codebase.

Builtins
--------

The ``future`` module provides these builtins as exact semantic equivalents on Python 2 to their Python 3 counterparts::

- open
- range, zip, map, filter
- super, round
- ascii, oct, hex, chr, input

Some of the ``future`` implementations are slower than the Python 3 equivalents.

The following differences exist between Python 3 builtins and Python 2 builtins::

The following are the remaining incompatibilities between Python 3 and Python 2 + ``future``. These are described below:

- bytes
- str
- int
- next
- metaclasses
- dictionary iterator methods


- bytes
-------
The Python 3 bytes object is substantially different from the Python 2 one::

  * bytes.__repr__ and bytes.__str__:
    bytes objects print with a b'' prefix like b'ABCD' on Py3.

  * casting to Unicode
    Python 3 often raises TypeErrors to guard against implicit type conversions
    from byte-strings to Unicode.

- str
-----
``future.builtins.str`` is an alias to Python 2's ``unicode`` type, which
behaves mostly similarly to Python 3's ``str`` object, with the following
differences:

- looser type-casting with ``bytes``. Py3 often raises a TypeError upon
  combining ``str`` with ``bytes`` in various ways.
- Superfluous (removed) decode() method
- Missing these methods that Py3 ``str`` defines:
  * casefold
  * format_map
  * isidentifier
  * isprintable
  * maketrans

``str(myobject)`` calls ``myobject.__str__()`` on Py3, whereas it calls ``myobject.__unicode__()`` on Py2 after ``from future.builtins import str``

Use the following decorator in front of classes which define their own ``__str__`` method to provide support for Py2::

@python_2_unicode_compatible
class MyClass(object):
    def __str__(self):
        return u'Unicode string here'

For more details of what this does, see here: http://link_here


- int
-----
Python 3 ``int`` is a unification of Python 2's ``int`` and
``long``. The major incompatibility is likely to be in doctests, where the Python 2 long representation has a trailing 'L':

Py3:
>>> 2**64
18446744073709551616

Py2:
>> 2**64
18446744073709551616L

To get the standard Py3 representation on Py2, you can import
``future.builtin_hacks.long``.

On Py3 or Py2:
    >>> from future.builtin_hacks import long
    >>> 2**64
    18446744073709551616


- next
------
On Python 3, consuming an iterator and calling the built-in ``next`` function
as ``next(myiter)`` both call ``myiter.__next__()``, whereas on Python 2 these
cal ``myiter.next()`` (without the underscores). To define a custom
iterator portably, apply the following decorator::

@implements_iterator
class MyIter(object):
    def __next__(self):
        ...

- metaclasses
-------------
Python 3 and Python 2 syntax for metaclasses are incompatible. The new syntax should ideally be available in Python 2 as a `__future__`` import like ``from __future__ import new_metaclass_syntax``. Since this is not available, ``future`` provides a function (from ``jinja2/_compat.py``) called ``with_metaclass`` that can assist with specifying metaclasses portably across Py3 and Py2. Use it like this::
        
    from future.utils import with_metaclass

    class BaseForm(object):
        pass
    
    class FormType(type):
        pass
    
    class Form(with_metaclass(FormType, BaseForm)):
        pass


- dictionary iterator methods
-----------------------------
If ``d`` is a small dictionary, use of ``d.keys()``, ``d.values()`` and ``d.items()`` is encouraged.

If ``d`` is a large dictionary for which the memory overhead of list creation from these methods on Python 2 is significant, then use the ``viewkeys()`` etc. functions from ``future.utils``::

    from future.utils import viewkeys, viewvalues, viewitems
    
    for (k, v) in viewitems(hugedictionary):
        ...

    These functions return view objects [ref] on both Py3 and Py2 which have set-like behaviour:

    >>> d = {i**2: i for i in range(1000)}
    >>> viewkeys(d) & set(range(0, 1000, 7))
    

[ref]: http://www.python.org/dev/peps/pep-3106/


