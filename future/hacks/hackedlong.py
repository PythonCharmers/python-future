from future.builtins import super
from future.hacks import hackclass, get_dict
from future.utils import PY3


if not PY3:
    # oldrepr = get_dict(long)['__repr__']
    # get_dict(long)['__oldrepr__'] = oldrepr
    # def newrepr(self):
    #     r = oldrepr(self)
    #     if r.endswith('L'):
    #         return r[:-1]
    #     else:
    #         return r
    # get_dict(long)['__repr__'] = newrepr
    get_dict(long)['tentimes'] = lambda x: x*10

    @hackclass(long, '__repr__')
    def repr(self):
        r = oldrepr(self)
        if r.endswith('L'):
            return r[:-1]
        else:
            return r


# Test:
# print(repr(2**64))
__all__ = []
