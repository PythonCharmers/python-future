"""
This module helps run Python 3.x-compatible code under Python 2.

It allows people to write clean, modern Python 3.x-compatible code today and to
run it with minimal effort under Python 2 alongside a Python 2 stack that may
contain dependencies that have not yet been ported to Python 3.

It is designed to be used as follows:

    from __future__ import division, absolute_import, print_function
    from future import common_iterators

Eventually, we may also support this:
    from future import standard_library

to bring in the new module names from the Python 3 standard library.

One goal is to help people migrate their codebases from Python 2.x to Python 3.

Python 3 offers a cleaner, better syntax and better organisation of the standard library.

Q. Who is this for?

A. 1. People who would prefer to write clean, future-proof Python
   3.x-compatible code, but whose day-jobs require that their code run on a
   Python 2 stack.

   2. People who wish to migrate their codebases easily, in a step-by-step
   fashion, to Python 3.

Q. What is the relationship between this project and python-modernize?

A. python-modernize is great, and this project is designed to complement it.
   For a project wishing to migrate to Python 3, python-modernize is useful for
   starting the process of cleaning up legacy code idioms and translating code
   into a more modern idiom: a subset of Python 3 and Python 2 that should run
   under either platform.

   This code is primarily designed to allow code authors to simplify their code
   as much as possible.

Q. What is the relationship between this project and six?

A. 'future' is a higher-level interface that builds on the six module. They
share the same goal of supporting codebases that work on both Python 2 and
Python 3 without modification. They differ in the interface they offer.

Six is a set of wrappers, so codebases that use it are not clean Python 3 code,
but a somewhat messy hybrid of Python 2, Python 3, and six-specific code.

Here is an example of code compatible with both Python 2 and Python 3 using six:

    from six.moves import xrange
    for i in xrange(10**8):
        pass

Here is the corresponding example using the 'future' module:

    from future import common_iterators
    for i in range(10**8):
        pass

Note that the latter example is standard Python 3 code, plus a one-line import.

Another difference is version support: 'future' supports only Python 2.6,
Python 2.7, and Python 3.3+. In contrast, six is designed to support versions
of Python prior to 2.6 and Python 3.0-3.2. Some of the interfaces provided by six (like the next() function) are not needed.

Consider another example:
    
    from six.moves import ...
    

Q. Is the goal for 'future' to backport more features of the standard library from Python 3.3+ to Python 2.6/2.7?

A. No. The initial goal is to support a subset of Python 3 rather than all of Python 3. This is mainly because of constraints on developer time, rather than ideological reasons. We wouldn't say No to pull requests.


Q. Can you support feature XYZ from the standard library in Python 3.3+ on Python 2.x?

A. Maybe. Our initial goal is to provide support for a subset of Python 3 code
on Python 2, to facilitate Python 3 adoption. Feel free to contribute code and
pull requests for further features.
"""

from __future__ import division, absolute_import, print_function

__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 1
__ver_sub__ = ''
__version__ = "%d.%d.%d%s" % (__ver_major__,__ver_minor__,__ver_patch__,__ver_sub__)

VERSION = __version__

__all__ = ['disable_obsolete_builtins', 'common_iterators', 'str_is_unicode']

