from future.hacks import hackclass, get_dict
from future import utils

if not utils.PY3:
    @hackclass(bytes, 'fromhex')
    def fromhex(*args):
        assert len(args) <= 2
        if len(args) == 0:
            raise TypeError('fromhex() takes exactly 1 argument (0 given)')
        string = args[-1]
        return string.replace(' ', '').decode('hex')
        # return b'\xff\xff'
    # get_dict(bytes)['fromhex'] = fromhex

    oldrepr = get_dict(bytes)['__repr__']

    @hackclass(bytes, '__repr__')
    def repr(self):
        return b'b' + oldrepr(self)

# print(repr(b''.fromhex('aa 0f')))
# print(repr(bytes.fromhex('b3 2e')))

# import pdb
# pdb.set_trace()

# if not utils.PY3:
#     def repr(self):
#         return b'b' + self.__oldrepr__()
#     get_dict(bytes)['__oldrepr__'] = get_dict(bytes)['__repr__']
#     get_dict(bytes)['__repr__'] = repr
#     # del get_dict(unicode)['decode']

# with hackclass_context(unicode, 'decode', lambda x: 1):
#     print(unicode(b'blah'))
#     print(u'abc'.decode('utf-8'))

