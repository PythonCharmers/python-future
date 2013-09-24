.. _future-imports:
Future imports
==============

Standard rubric
~~~~~~~~~~~~~~~

The imports to include at the top of every future-compatible Py3/2 module are::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future import standard_library
    from future.builtins import *

On Python 3, these import lines have zero effect and zero namespace
pollution.

On Python 2, ``from future import standard_library`` installs
import hooks to allow renamed and moved standard library modules to be
imported from their new Py3 locations. See :ref:`standard-library` for more
information.

On Python 2, the ``from future.builtins import *`` line shadows builtins
to provide their Python 3 semantics. (See :ref:`explicit-imports` for the
explicit form.)


__future__ imports
~~~~~~~~~~~~~~~~~~

For more information about the ``__future__`` imports, which are a standard
feature of Python, see the following docs:

- absolute_import: `PEP 328: Imports: Multi-Line and Absolute/Relative <http://www.python.org/dev/peps/pep-0328>`_
- division: `PEP 238: Changing the Division Operator <http://www.python.org/dev/peps/pep-0238>`_
- print_function: `PEP 3105: Make print a function <http://www.python.org/dev/peps/pep-3105>`_
- unicode_literals: `PEP 3112: Bytes literals in Python 3000 <http://www.python.org/dev/peps/pep-3112>`_

These are all available in Python 2.6 and up, and mandatory in Python 3+.


.. _explicit-imports:
Explicit imports
~~~~~~~~~~~~~~~~
If you prefer explicit imports, the explicit equivalent of the ``from
future.builtins import *`` line is::

    from future.builtins import (zip, map, filter,
                                 ascii, oct, hex, chr, input,
                                 bytes, range, super, round,
                                 apply, cmp, coerce, execfile, file, long,
                                 raw_input, reduce, reload, unicode, xrange,
                                 str, StandardError)

To understand what each of these does, see the docs for these modules:

- future.builtins
- future.builtins.iterators
- future.builtins.misc
- future.builtins.backports
- future.builtins.disabled
- future.builtins.str_is_unicode

The internal API is currently as follows::
    
    from future.builtins.iterators import zip, map, filter
    from future.builtins.misc import ascii, oct, hex, chr, input
    from future.builtins.backports import bytes, range, super, round
    from future.builtins.disabled import (apply, cmp, coerce,
            execfile, file, long, raw_input, reduce, reload, unicode,
            xrange, StandardError)
    from future.builtins.str_is_unicode import str

But please note that this internal API is not stable between different versions
of ``future``.

