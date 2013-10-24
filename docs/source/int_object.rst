.. _int-object:

int
---

Python 3's ``int`` type is very similar to Python 2's ``long``, except
for the representation (which omits the ``L`` suffix in Python 2). Python
2's normal (short) integers have been removed from Python 3.

``future`` includes a backport of Python 3's ``int`` since v0.7.0, which
is a subclass of Python 2's ``long`` with the same representation
behaviour. To ensure an integer is long compatibly both Py3 and Py2, cast
it like this::

    >>> from future.builtins import *
    >>> must_be_a_long_integer = int(1234)

This simplifies code that deals with ``long`` and ``int`` as special
cases on Py2. An example is the following code from ``xlwt-future`` (which is
called by the ``xlwt.antlr.BitSet`` class), which must use long integers.

With ``future`` v0.7.0+, this becomes::

    def longify(data):
        """
        Turns data (an int or long, or a list of ints or longs) into a
        list of longs.
        """
        if not data:
            return [int(0)]
        if not isinstance(data,list):
            return [int(data)]
        return list(map(int, data))


Without ``future`` (or with ``future`` < 0.7), this might be::

    def longify(data):
        """
        Turns data (an int or long, or a list of ints or longs) into a
        list of longs.
        """
        if not data:
            if PY3:
                return [0]
            else:
                return [long(0)]
        if not isinstance(data,list):
            if PY3:
                return [int(data)]
            else:
                return [long(data)]
        if PY3:
            return list(map(int, data))   # same as returning data, but with up-front typechecking
        else:
            return list(map(long, data))


The redefinition of ``int`` has the side-effect of breaking ``isinstance(x, int)``
calls for Python 2's short integers. See :ref:`isinstance-calls`.

