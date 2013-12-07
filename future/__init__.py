"""
future: Easy, safe support for Python 2/3 compatibility
=======================================================

``future`` is the missing compatibility layer between Python 2 and Python 3. It allows you to use a single, clean Python 3.x-compatible codebase to support both Python 2 and Python 3 with minimal overhead.

Notable projects that use ``future`` for Python 2/3 compatibility are `Mezzanine <http://mezzanine.jupo.org/>`_ and `xlwt-future <https://pypi.python.org/pypi/xlwt-future>`_.

It is designed to be used as follows::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future import standard_library
    from future.builtins import *     # or explicit imports: str, int, bytes,
                                      # open, super, range, zip, input, etc.
    
followed by predominantly standard, idiomatic Python 3 code that then runs similarly on Python 2.6/2.7 and Python 3.3+.

On Python 3, the import lines have zero effect (and zero namespace
pollution).

On Python 2, ``from future import standard_library`` installs
import hooks to allow renamed and moved standard library modules to be
imported from their new Py3 locations. On Python 2, the ``from future.builtins import *`` line shadows all builtins with different behaviour in Python 3 versus 2 to provide their Python 3 semantics.


Automatic conversion
--------------------
An included script called `futurize <http://python-future.org/automatic_conversion.html>`_ aids in converting code (from either Python 2 or Python 3) to code compatible with both platforms. It is similar to ``python-modernize`` but goes further in providing Python 3 compatibility through the use of the backported types and builtin functions in ``future``.


Documentation
-------------

See: http://python-future.org

Also see the docstrings for each of these modules for more info::

- future.standard_library
- future.builtins
- future.utils


Credits
-------

:Author:  Ed Schofield
:Sponsor: Python Charmers Pty Ltd, Australia, and Python Charmers Pte
          Ltd, Singapore. http://pythoncharmers.com
:Others:  - The backported ``super()`` and ``range()`` functions are
            derived from Ryan Kelly's ``magicsuper`` module and Dan
            Crosta's ``xrange`` module.
          - The ``futurize`` script uses ``lib2to3`` and fixers from
            Joe Amenta's ``lib3to2`` and Armin Ronacher's ``python-modernize``.
          - The ``python_2_unicode_compatible`` decorator is from
            Django. The ``implements_iterator`` and ``with_metaclass``
            decorators are from Jinja2.
          - Documentation is generated using ``sphinx`` and styled using
            ``sphinx-bootstrap-theme``.


Licensing
---------
Copyright 2013 Python Charmers Pty Ltd, Australia.
The software is distributed under an MIT licence. See LICENSE.txt.

"""

# No namespace pollution
__all__ = []

__ver_major__ = 0
__ver_minor__ = 10
__ver_patch__ = 1
__ver_sub__ = ''
__version__ = "%d.%d.%d%s" % (__ver_major__, __ver_minor__,
                              __ver_patch__, __ver_sub__)

