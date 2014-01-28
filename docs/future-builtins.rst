.. _future-builtins:

``future.builtins``
===================

- ``pow()`` supports fractional exponents of negative numbers like in Py3::

    >>> from future.builtins import pow
    >>> pow(-1, 0.5)
    (6.123233995736766e-17+1j)

- ``round()`` uses Banker's Rounding as in Py3 to the nearest even last digit::

    >>> from future.builtins import round
    >>> assert round(0.1250, 2) == 0.12

