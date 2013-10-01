"""
``python-future``: pure Python implementation of Python 3 round().
"""
 
def newround(number, ndigits=None):
    """
    See Python 3 documentation: uses Banker's Rounding.
 
    Delegates to the __round__ method if for some reason this exists.
 
    If not, rounds a number to a given precision in decimal digits (default
    0 digits). This returns an int when called with one argument,
    otherwise the same type as the number. ndigits may be negative.
 
    See the test_round method in future/tests/test_builtins.py for
    examples.
    """
    return_int = False
    if ndigits is None:
        return_int = True
        ndigits = 0
    if hasattr(number, '__round__'):
        return number.__round__(ndigits)
    
    # Use the decimal module for simplicity of implementation (and
    # hopefully correctness).
    from decimal import Decimal, ROUND_HALF_EVEN
 
    if ndigits < 0:
        raise NotImplementedError('negative ndigits not supported yet')
    exponent = Decimal('10') ** (-ndigits)
    d = Decimal.from_float(number).quantize(exponent,
                                            rounding=ROUND_HALF_EVEN)
    if return_int:
        return int(d)
    else:
        return float(d)
 

__all__ = ['newround']
