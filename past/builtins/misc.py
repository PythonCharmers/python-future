from __future__ import unicode_literals
import sys

from future.utils import PY3, exec_


if PY3:
    def apply(f, *args, **kw):
        return f(*args, **kw)
    from past.builtins import str as oldstr
    def chr(i):
        """
        Return a byte-string of one character with ordinal i; 0 <= i <= 256
        """
        return oldstr(bytes((i,)))
    cmp = lambda a, b: (a > b) - (a < b)
    from sys import intern
    raw_input = input
    from imp import reload
    unicode = str
    unichr = chr
    xrange = range
else:
    import __builtin__
    apply = __builtin__.apply
    chr = __builtin__.chr
    cmp = __builtin__.cmp
    execfile = __builtin__.execfile
    intern = __builtin__.intern
    raw_input = __builtin__.raw_input
    reload = __builtin__.reload
    unicode = __builtin__.unicode
    unichr = __builtin__.unichr
    xrange = __builtin__.xrange


if PY3:
    def execfile(filename, myglobals=None, mylocals=None):
        """
        A version of execfile() that handles unicode filenames.
        From IPython.

        WARNING: This doesn't seem to work. We may need to use inspect to
        get the globals and locals dicts from the calling context.
        """
        mylocals = mylocals if (mylocals is not None) else myglobals
        exec_(compile(open(filename).read(), filename, 'exec'),
              myglobals, mylocals)

# else:
#     def execfile(filename, myglobals=None, mylocals=None):
#         """
#         A version of execfile() for Py2 that handles unicode filenames.
#         This is useful if "from __future__ import unicode_literals" is in
#         effect.
# 
#         From IPython.
#         """
#         if sys.platform == 'win32':
#             # The rstrip() is necessary b/c trailing whitespace in
#             # files will cause an IndentationError in Python 2.6
#             # (this was fixed in 2.7). See IPython issue 1027.
#             scripttext = __builtin__.open(filename).read().rstrip() + '\n'
#             # compile converts unicode filename to str assuming
#             # ascii. Let's do the conversion before calling compile
#             if isinstance(filename, unicode):
#                 filename = filename.encode(unicode, 'replace')
#             # else:
#             #     filename = filename
#             exec_(compile(scripttext, filename, 'exec') in glob, loc)
#         else:
#             if isinstance(filename, unicode):
#                 filename = filename.encode(sys.getfilesystemencoding())
#             else:
#                 filename = filename
#             if mylocals is not None:
#                 if myglobals is not None:
#                     __builtin__.execfile(filename, myglobals, mylocals)
#                 else:
#                     raise ValueError(
#                         'globals argument is required if locals is passed')
#             else:
#                 if myglobals is not None:
#                     __builtin__.execfile(filename, myglobals)
#                 else:
#                     __builtin__.execfile(filename)

if PY3:
    __all__ = ['apply', 'chr', 'cmp', 'execfile', 'intern', 'raw_input',
               'reload', 'unichr', 'unicode', 'xrange']
else:
    __all__ = []

