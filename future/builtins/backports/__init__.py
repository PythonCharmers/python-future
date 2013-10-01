"""
This module contains backports of new or changed functionality from
Python 3 to Python 2.

For example:
- an implementation of Python 3's bytes object (pure Python subclass of
  Python 2's builtin 8-bit str type)
- a backport of the range iterator from Py3 with slicing support
- the magic zero-argument super() function
- the new round() behaviour

It is used as follows::

    from __future__ import division, absolute_import, print_function
    from future.builtins.backports import bytes, range, super, round

to bring in the new semantics for these functions from Python 3. And
then, for example::
    
    b = bytes(b'ABCD')
    assert list(b) == [65, 66, 67, 68]
    assert repr(b) == "b'ABCD'"
    assert [65, 66] in b

    # These raise TypeErrors:
    # b + u'EFGH'
    # b.split(u'B')
    # bytes(b',').join([u'Fred', u'Bill'])

    for i in range(10**11)[:10]:
        pass

and::
    
    class VerboseList(list):
        def append(self, item):
            print('Adding an item')
            super().append(item)        # new simpler super() function

Notes
=====

range()
-------
``range`` is a custom class that backports the slicing behaviour from
Python 3 (based on the ``xrange`` module by Dan Crosta). See the
``newrange`` module docstring for more details.


super()
-------
``super()`` is based on Ryan Kelly's ``magicsuper`` module. See the
``newsuper`` module docstring for more details.


input()
-------
Like the new ``input()`` function from Python 3 (without eval()), except
that it returns bytes. Equivalent to Python 2's ``raw_input()``.

Warning: By default, importing this module *removes* the old Python 2
input() function entirely from ``__builtin__`` for safety. This is
because forgetting to import the new ``input`` from ``future`` might
otherwise lead to a security vulnerability (shell injection) on Python 2.

To restore it, you can retrieve it yourself from
``__builtin__._old_input``.

Fortunately, ``input()`` seems to be seldom used in the wild in Python
2...


round()
-------
Python 3 modifies the behaviour of ``round()`` to use "Banker's Rounding".
See http://stackoverflow.com/a/10825998_. See the ``newround`` module
docstring for more details.


TODO:
-----
- Check int() ??

"""

from __future__ import division, absolute_import, print_function

import functools

from future import utils


# Some utility functions to enforce strict type-separation of unicode str and
# bytes:
def disallow_types(argnums, disallowed_types):
    """
    A decorator that raises a TypeError if any of the given arguments is
    of the given type (e.g. bytes or unicode string).

    Example use:

    >>> class newbytes(object):
    ...     @disallow_types([1], [unicode])
    ...     def __add__(self, other):
    ...          pass

    >>> newbytes('1234') + u'1234'      #doctest: +IGNORE_EXCEPTION_DETAIL 
    Traceback (most recent call last):
      ...
    TypeError: can't concat 'bytes' to (unicode) str
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            errmsg = "argument can't be {}"
            for (argnum, mytype) in zip(argnums, disallowed_types):
                if isinstance(args[argnum], mytype):
                    raise TypeError(errmsg.format(mytype))
            return function(*args, **kwargs)
        return wrapper
    return decorator


def no(mytype, argnums=(1,)):
    """
    A shortcut for the disallow_types decorator that disallows only one type
    (in any position in argnums).

    Example use:

    >>> class newstr(object):
    ...     @no(bytes)
    ...     def __add__(self, other):
    ...          pass

    >>> newstr(u'1234') + b'1234'     #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    TypeError: argument can't be bytes
    """
    if isinstance(argnums, int):
        argnums = (argnums,)
    disallowed_types = [mytype] * len(argnums)
    return disallow_types(argnums, disallowed_types)


def issubset(list1, list2):
    """
    Examples:

    >>> issubset([], [65, 66, 67])
    True
    >>> issubset([65], [65, 66, 67])
    True
    >>> issubset([65, 66], [65, 66, 67])
    True
    >>> issubset([65, 67], [65, 66, 67])
    False
    """
    n = len(list1)
    for startpos in range(len(list2) - n + 1):
        if list2[startpos:startpos+n] == list1:
            return True
    return False


if utils.PY3:
    import builtins
    str = builtins.str
    bytes = builtins.bytes
    range = builtins.range
    round = builtins.round
    super = builtins.super
    __all__ = []
else:
    from .newbytes import bytes
    from .newrange import range
    from .newsuper import super
    from .newround import round
    __all__ = ['bytes', 'range', 'super', 'round']
