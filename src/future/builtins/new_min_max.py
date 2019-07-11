from future import utils
if utils.PY2:
    from __builtin__ import max as _builtin_max, min as _builtin_min
else:
    from builtins import max as _builtin_max, min as _builtin_min


def newmin(*args, **kwargs):
    return new_min_max(_builtin_min, *args, **kwargs)


def newmax(*args, **kwargs):
    return new_min_max(_builtin_max, *args, **kwargs)


def new_min_max(_builtin_func, *args, **kwargs):
    """
    To support the argument "default" introduced in python 3.4 for min and max
    :param _builtin_func: builtin min or builtin max
    :param args:
    :param kwargs:
    :return: returns the min or max based on the arguments passed
    """

    for key, _ in kwargs.items():
        if key not in set(['key', 'default']):
            raise TypeError('Illegal argument %s', key)

    if len(args) == 0:
        raise TypeError

    if len(args) != 1 and kwargs.get('default') is not None:
        raise TypeError

    if len(args) == 1:
        try:
            next(iter(args[0]))
        except StopIteration:
            if kwargs.get('default') is not None:
                return kwargs.get('default')
            else:
                raise ValueError('iterable is an empty sequence')
        if kwargs.get('key') is not None:
            return _builtin_func(args[0], key=kwargs.get('key'))
        else:
            return _builtin_func(args[0])

    if len(args) > 1:
        if kwargs.get('key') is not None:
            return _builtin_func(args, key=kwargs.get('key'))
        else:
            return _builtin_func(args)
