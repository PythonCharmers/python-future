"""
Nearly identical to xrange.py, by Dan Crosta, from 

    https://github.com/dcrosta/xrange.git

This is included here in the ``future`` package rather than pointed to as
a dependency because there is no package for ``xrange`` on PyPI. It is
also tweaked to appear like a regular Python 3 ``range`` object rather
than a Python 2 xrange.

From Dan Crosta's README:

    "A pure-Python implementation of Python 2.7's xrange built-in, with
    some features backported from the Python 3.x range built-in (which
    replaced xrange) in that version."

    Read more at
        https://late.am/post/2012/06/18/what-the-heck-is-an-xrange
"""

from math import ceil
from collections import Sequence, Iterator

from future.utils import PY3


class newrange(Sequence):
    """
    Pure-Python backport of Python 3's range object.  See `the CPython
    documentation for details:
        <http://docs.python.org/py3k/library/functions.html#range>`_
    """

    def __init__(self, *args):
        if len(args) == 1:
            start, stop, step = 0, args[0], 1
        elif len(args) == 2:
            start, stop, step = args[0], args[1], 1
        elif len(args) == 3:
            start, stop, step = args
        else:
            raise TypeError('range() requires 1-3 int arguments')

        try:
            start, stop, step = int(start), int(stop), int(step)
        except ValueError:
            raise TypeError('an integer is required')

        if step == 0:
            raise ValueError('range() arg 3 must not be zero')
        elif step < 0:
            stop = min(stop, start)
        else:
            stop = max(stop, start)

        self._start = start
        self._stop = stop
        self._step = step
        self._len = (stop - start) // step + bool((stop - start) % step)

    def __repr__(self):
        if self._start == 0 and self._step == 1:
            return 'range(%d)' % self._stop
        elif self._step == 1:
            return 'range(%d, %d)' % (self._start, self._stop)
        return 'range(%d, %d, %d)' % (self._start, self._stop, self._step)

    def __eq__(self, other):
        return isinstance(other, newrange) and \
               self._start == other._start and \
               self._stop == other._stop and \
               self._step == other._step

    def __len__(self):
        return self._len

    def index(self, value):
        """Return the 0-based position of integer `value` in
        the sequence this range represents."""
        diff = value - self._start
        quotient, remainder = divmod(diff, self._step)
        if remainder == 0 and 0 <= quotient < self._len:
            return abs(quotient)
        raise ValueError('%r is not in range' % value)

    def count(self, value):
        """Return the number of ocurrences of integer `value`
        in the sequence this range represents."""
        # a value can occur exactly zero or one times
        return int(value in self)

    def __contains__(self, value):
        """Return ``True`` if the integer `value` occurs in
        the sequence this range represents."""
        try:
            self.index(value)
            return True
        except ValueError:
            return False

    def __reversed__(self):
        """Return a range which represents a sequence whose
        contents are the same as the sequence this range
        represents, but in the opposite order."""
        sign = self._step / abs(self._step)
        last = self._start + ((self._len - 1) * self._step)
        return newrange(last, self._start - sign, -1 * self._step)

    def __getitem__(self, index):
        """Return the element at position ``index`` in the sequence
        this range represents, or raise :class:`IndexError` if the
        position is out of range."""
        if isinstance(index, slice):
            return self.__getitem_slice(index)
        if index < 0:
            # negative indexes access from the end
            index = self._len + index
        if index < 0 or index >= self._len:
            raise IndexError('range object index out of range')
        return self._start + index * self._step

    def __getitem_slice(self, slce):
        """Return a range which represents the requested slce
        of the sequence represented by this range.
        """
        start, stop, step = slce.start, slce.stop, slce.step
        if step == 0:
            raise ValueError('slice step cannot be 0')

        start = start or self._start
        stop = stop or self._stop
        if start < 0:
            start = max(0, start + self._len)
        if stop < 0:
            stop = max(start, stop + self._len)

        if step is None or step > 0:
            return newrange(start, stop, step or 1)
        else:
            rv = reversed(self)
            rv._step = step
            return rv

    def __iter__(self):
        """Return an iterator which enumerates the elements of the
        sequence this range represents."""
        return rangeiterator(self)


class rangeiterator(Iterator):
    """An iterator for a :class:`range`.
    """

    def __init__(self, rangeobj):
        self._range = rangeobj

        # Intialize the "last outputted value" to the value
        # just before the first value; this simplifies next()
        self._last = self._range._start - self._range._step
        self._count = 0

    def __iter__(self):
        """An iterator is already an iterator, so return ``self``.
        """
        return self

    def next(self):
        """Return the next element in the sequence represented
        by the range we are iterating, or raise StopIteration
        if we have passed the end of the sequence."""
        self._last += self._range._step
        self._count += 1
        if self._count > self._range._len:
            raise StopIteration()
        return self._last


__all__ = ['newrange']
