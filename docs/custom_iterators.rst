.. _custom-iterators:

Custom iterators
----------------

If you define your own iterators, there is an incompatibility in the method name
across Py3 and Py2. On Python 3 it is ``__next__``, whereas on Python 2 it is
``next``.

The ``next`` function in ``future.builtins`` provides compatibility across
Python 2 and Python 3 for iterators that defines a Python 3-like ``.__next__``
method. You can use it as follows::

    # Python 3-style iterator:
    class Upper(object):
        def __init__(self, iterable):
            self._iter = iter(iterable)
        def __next__(self):                 # note the Py3 interface
            return next(self._iter).upper()
        def __iter__(self):
            return self

    from future.builtins import next
    itr = Upper('hello')
    assert next(itr) == 'H'
    assert next(itr) == 'E'

``next()`` also works with regular Python 2 iterators with a ``.next`` method::

    itr = iter(['one', 'three', 'five'])
    assert 'next' in dir(itr)
    assert next(itr) == 'one'

This works whenever your code calls the ``next()`` function explicitly.  If you
consume the iterator implicitly in a ``for`` loop or ``list()`` call or by some
other method, the ``future.builtins.next`` function will not help.  Instead, a
decorator called ``implements_iterator`` is provided in ``future.utils`` to
allow Py3-style iterators to work identically on Py2. Use it as follows::

    from future.utils import implements_iterator

    Upper = implements_iterator(Upper)

    print(list(Upper('hello')))
    # prints ['H', 'E', 'L', 'L', 'O']

This can of course also be used with the ``@`` decorator syntax when defining
the iterator as follows::

    @implements_iterator
    class Upper(object):
        def __init__(self, iterable):
            self._iter = iter(iterable)
        def __next__(self):                 # note the Py3 interface
            return next(self._iter).upper()
        def __iter__(self):
            return self

On Python 3, as usual, this decorator does nothing.

