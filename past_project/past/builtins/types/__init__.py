from past import utils

if utils.PY2:
    import __builtin__
    basestring = __builtin__.basestring
    dict = __builtin__.dict
    str = __builtin__.str
    __all__ = []
else:
    from .basestring import basestring
    from .olddict import olddict as dict
    from .oldstr import oldstr as str
    # from .unicode import unicode
    __all__ = ['basestring', 'dict', 'str']

