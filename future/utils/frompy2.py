"""
A resurrection of old from Python 2 for both platforms.

"""

from __future__ import unicode_literals

from future.utils import PY3


if PY3:
    # Bring back the cmp function
    cmp = lambda a, b: (a > b) - (a < b)
    unicode = str
else:
    cmp = __builtin__.cmp
    unicode = __builtin__.unicode


def execfile(filename, myglobals=None, mylocals=None):
    if PY3:
        mylocals = mylocals if (mylocals is not None) else myglobals
        exec_(compile(open(filename).read(), filename, 'exec'),
              myglobals, mylocals)
    else:
        if sys.platform == 'win32':
            # The rstrip() is necessary b/c trailing whitespace in
            # files will cause an IndentationError in Python 2.6
            # (this was fixed in 2.7). See IPython issue 1027.
            scripttext = __builtin__.open(filename).read().rstrip() + '\n'
            # compile converts unicode filename to str assuming
            # ascii. Let's do the conversion before calling compile
            if isinstance(filename, unicode):
                filename = filename.encode(unicode, 'replace')
            # else:
            #     filename = filename
            exec_(compile(scripttext, filename, 'exec') in glob, loc)
        else:
            if isinstance(filename, unicode):
                filename = filename.encode(sys.getfilesystemencoding())
            else:
                filename = filename
            __builtin__.execfile(filename, myglobals=myglobals,
                                 mylocals=mylocals)

if PY3:
    __all__ = []
else:
    __all__ = ['cmp', 'unicode', 'execfile']

