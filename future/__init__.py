"""
future: clean single-source support for Python 3 and 2
======================================================

The ``future`` module helps run Python 3.x-compatible code under Python 2
with minimal code cruft.

The goal is to allow you to write clean, modern, forward-compatible
Python 3 code today and to run it with minimal effort under Python 2
alongside a Python 2 stack that may contain dependencies that have not
yet been ported to Python 3.

It is designed to be used as follows::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future import standard_library
    from future.builtins import *
    
followed by clean Python 3 code (with a few restrictions) that can run
unchanged on Python 2.7.

On Python 3, the import lines have zero effect (and zero namespace
pollution).

On Python 2, ``from future import standard_library`` installs
import hooks to allow renamed and moved standard library modules to be
imported from their new Py3 locations.

On Python 2, the ``from future.builtins import *`` line shadows builtins
to provide their Python 3 semantics. (See below for the explicit import
form.)

Documentation
-------------

See: http://python-future.org

Also see the docstrings for each of these modules for more info::

- future.standard_library
- future.builtins
- future.utils


Automatic conversion
--------------------
An experimental script called ``futurize`` is included to aid in making
either Python 2 code or Python 3 code compatible with both platforms
using the ``future`` module. See `<http://python-future.org/automatic_conversion.html>`_.


Credits
-------

:Author:  Ed Schofield
:Sponsor: Python Charmers Pty Ltd, Australia, and Python Charmers Pte
          Ltd, Singapore. http://pythoncharmers.com
:Others:  - The backported ``super()`` and ``range()`` functions are
            derived from Ryan Kelly's ``magicsuper`` module and Dan
            Crosta's ``xrange`` module.
          - The ``futurize`` script uses ``lib2to3``, ``lib3to2``, and
            parts of Armin Ronacher's ``python-modernize`` code.
          - The ``python_2_unicode_compatible`` decorator is from
            Django. The ``implements_iterator`` and ``with_metaclass``
            decorators are from Jinja2.
          - ``future`` incorporates the ``six`` module by Benjamin
            Peterson as ``future.utils.six``.
          - Documentation is generated using ``sphinx`` using an
            adaptation of Armin Ronacher's stylesheets from Jinja2.


Licensing
---------
Copyright 2013 Python Charmers Pty Ltd, Australia.
The software is distributed under an MIT licence. See LICENSE.txt.

"""

# No namespace pollution
__all__ = []

__ver_major__ = 0
__ver_minor__ = 9
__ver_patch__ = 0
__ver_sub__ = ''
__version__ = "%d.%d.%d%s" % (__ver_major__, __ver_minor__,
                              __ver_patch__, __ver_sub__)

