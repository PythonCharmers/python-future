"""
Miscellaneous function (re)definitions from the Py3.3 standard library for
Python 2.6/2.7.
"""
from math import ceil as oldceil

def ceil(x):
    """
    Return the ceiling of x as an int.
    This is the smallest integral value >= x.
    """
    return int(oldceil(x))


try:
    from functools import cmp_to_key
except ImportError: # <= Python 2.6
    def cmp_to_key(mycmp):
        """
        Convert a cmp= function into a key= function
        """
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj

            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0

            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0

            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0

            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0

            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0

            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K


# subprocess.check_output() is new in Python 2.7
import os

try:
    try:
        from subprocess import check_output
    except ImportError: # <= Python 2.6
        from subprocess import CalledProcessError, check_call
        def check_output(*args, **kwargs):
            with open(os.devnull, 'w') as fh:
                kwargs['stdout'] = fh
                try:
                    return check_call(*args, **kwargs)
                except CalledProcessError as e:
                    e.output = ("program output is not available for Python 2.6.x")
                    raise e
except ImportError:
    # running on platform like App Engine, no subprocess at all
    pass


try:
    from itertools import combinations_with_replacement
except ImportError:  # <= Python 2.6
    def combinations_with_replacement(iterable, r):
        """Return r length subsequences of elements from the input iterable
        allowing individual elements to be repeated more than once.

        Combinations are emitted in lexicographic sort order. So, if the
        input iterable is sorted, the combination tuples will be produced
        in sorted order.

        Elements are treated as unique based on their position, not on their
        value. So if the input elements are unique, the generated combinations
        will also be unique.

        See also: combinations

        Examples
        ========

        >>> from future.backports.misc import combinations_with_replacement
        >>> list(combinations_with_replacement('AB', 2))
        [('A', 'A'), ('A', 'B'), ('B', 'B')]
        """
        pool = tuple(iterable)
        n = len(pool)
        if not n and r:
            return
        indices = [0] * r
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != n - 1:
                    break
            else:
                return
            indices[i:] = [indices[i] + 1] * (r - i)
            yield tuple(pool[i] for i in indices)

