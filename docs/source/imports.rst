.. _imports:

Imports
=======

future imports
~~~~~~~~~~~~~~

The imports to include at the top of every future-compatible Py3/2
module are::

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

For more information about the ``__future__`` imports, which are a
standard feature of Python, see the following docs:

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
                                 ascii, oct, hex, chr, int, input, open,
                                 str, bytes, range, round, super,
                                 apply, cmp, coerce, execfile, file, long,
                                 raw_input, reduce, reload, unicode, xrange,
                                 StandardError)

However, we discourage importing only some of these builtins because this
increases the risk of introducing Py2/3 portability bugs into your code.

To understand what each of these does, see the docs for these modules:

- future.builtins
- future.builtins.iterators
- future.builtins.misc
- future.builtins.backports
- future.builtins.disabled

The internal API is currently as follows::

    from future.builtins.iterators import filter, map, zip
    from future.builtins.misc import ascii, chr, hex, input, int, oct, open
    from future.builtins.backports import bytes, range, round, str, super
    from future.builtins.disabled import (apply, cmp, coerce,
            execfile, file, long, raw_input, reduce, reload, unicode,
            xrange, StandardError)

But please note that this internal API is evolving and may not be stable
between different versions of ``future``.

