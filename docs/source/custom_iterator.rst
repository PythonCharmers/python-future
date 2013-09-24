Custom iterators
----------------

If you define your own iterator, there is an incompatibility in the method name
across Py3 and Py2. On Python 3 it is ``__next__``, whereas on Python 2 it is
``next``.

Use the following decorator to allow Py3-style iterators to work
identically on Py2::

    from future.utils import implements_iterator

    @implements_iterator
    class Upper(object):
        def __init__(self, iterable):
            self._iter = iter(iterable)
        def __next__(self):                 # note the Py3 interface
            return next(self._iter).upper()
        def __iter__(self):
            return self

    print(list(Upper('hello')))
    # prints ['H', 'E', 'L', 'L', 'O']

On Python 3 this decorator does nothing (no-op).

