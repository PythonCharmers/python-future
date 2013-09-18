"""
A resurrection of some old functions from Python 2. These should be used
sparingly, to help with porting efforts, since code using them is no
longer standard Python 3 code.

We provide these builtin functions which have no equivalent on Py3:

- cmp()
- execfile()

These aliases are also provided:

- raw_input() <- input()
- unicode() <- str()
- unichr() <- chr()

For reference, the following Py2 builtin functions are available from
these standard locations on both Py2.6+ and Py3:

- reduce() <- functools.reduce()
- reload() <- imp.reload()

"""

from __future__ import unicode_literals

from future.utils import PY3


if PY3:
    # Bring back the cmp function
    cmp = lambda a, b: (a > b) - (a < b)
    raw_input = input
    unicode = str
    unichr = chr
else:
    cmp = __builtin__.cmp
    raw_input = __builtin__.raw_input
    unicode = __builtin__.unicode
    unichr = __builtin__.unichr


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


__all__ = ['cmp', 'raw_input', 'unichr', 'unicode', 'execfile']
