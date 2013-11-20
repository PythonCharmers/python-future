.. _dict-object:

Backported ``dict`` type
------------------------

``future.builtins`` provides a Python 2 ``dict`` subclass whose :func:`keys`,
:func:`values`, and :func:`items` methods have the same set-like view behaviour
on Python 2.7 as on Python 3. This can streamline code needing
to iterate over large dictionaries. For example::

    from __future__ import print_function
    from future.builtins import dict, range
    
    # Currently, this requires (and then frees) a large amount of temporary
    # memory:
    d = dict({i: i**2 for i in range(10**7)})

    # Memory-efficient construction:
    d = dict((i, i**2) for i in range(10**7))
    
    assert not isinstance(d.items(), list)
    
    # Because items() is memory-efficient, so is this:
    d2 = dict((i_squared, i) for (i, i_squared) in d.items())


On Python 2.6, these methods currently return iterators that do not support the
new Py3 set-like behaviour.

