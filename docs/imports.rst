.. _imports:

Imports
=======

future imports
~~~~~~~~~~~~~~

The easiest way to provide Py2/3 compatibility using ``future`` is to
include the following imports at the top of every module::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future import *

On Python 3, ``from future import *`` imports only two symbols: the modules
``standard_library`` and ``utils``. No builtin functions are affected.

On Python 2, this import line also shadows 16 builtins (listed below) to
provide their Python 3 semantics.


More explicit imports
~~~~~~~~~~~~~~~~~~~~~

If you wish to be avoid namespace pollution on Python 3, an alternative set
of imports is::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future.builtins import *

together with these module imports when necessary::
    
    from future import standard_library, utils

The advantage of this form is that on Python 3, the ``from future.builtins
import *`` line has zero effect and zero namespace pollution.

On Python 2, ``from future.builtins import *`` shadows the same builtins
(see below) as with ``from future import *``.


.. _explicit-imports:

Explicit imports
~~~~~~~~~~~~~~~~

If you prefer fully explicit imports, the most common set is::
    
    from future import standard_library, utils
    from future.builtins import (bytes, int, range, round, str, super,
                                 ascii, chr, hex, input, oct, open,
                                 filter, map, zip)

All the replaced builtins are also available in the ``future`` namespace.

The disadvantage of importing only some of the builtins is that it
increases the risk of introducing Py2/3 portability bugs as your code
evolves over time. Be especially aware of ``input``, which could expose a
security vulnerability on Python 2 without the ``future`` import.

Also, a technical distinction is that unlike the ``import *`` forms above,
these explicit imports do actually change ``locals()``; this is equivalent
to typing ``filter = filter; map = map`` etc. for each builtin.

To understand the details of the backported builtins on Python 2, see the
docs for these modules:

- future.builtins
- future.builtins.iterators
- future.builtins.misc
- future.builtins.backports

The internal API is currently as follows::

    from future.builtins.backports import bytes, int, range, round, str, super
    from future.builtins.misc import ascii, chr, hex, input, oct, open
    from future.builtins.iterators import filter, map, zip

(Please note that this internal API is evolving and may not be stable
between different versions of ``future``.)


.. _obsolete-builtins:

Obsolete Python 2 builtins
~~~~~~~~~~~~~~~~~~~~~~~~~~

Twelve Python 2 builtins have been removed from Python 3. To aid with
porting code to Python 3 module by module, you can use the following
import to cause a ``NameError`` exception to be raised on Python 2 when any
of the obsolete builtins is used, just as would occur on Python 3::

    from future.builtins.disabled import *

This is equivalent to::

    from future.builtins.disabled import (apply, cmp, coerce, execfile,
                                 file, long, raw_input, reduce, reload,
                                 unicode, xrange, StandardError)

Running ``futurize`` over code that uses these Python 2 builtins does not
import the disabled versions; instead, it replaces them with their
equivalent Python 3 forms and then adds ``future`` imports to resurrect
Python 2 support.


__future__ imports
~~~~~~~~~~~~~~~~~~

For more information about the ``__future__`` imports, which are a
standard feature of Python, see the following docs:

- absolute_import: `PEP 328: Imports: Multi-Line and Absolute/Relative <http://www.python.org/dev/peps/pep-0328>`_
- division: `PEP 238: Changing the Division Operator <http://www.python.org/dev/peps/pep-0238>`_
- print_function: `PEP 3105: Make print a function <http://www.python.org/dev/peps/pep-3105>`_
- unicode_literals: `PEP 3112: Bytes literals in Python 3000 <http://www.python.org/dev/peps/pep-3112>`_

These are all available in Python 2.6 and up, and enabled by default in Python 3.x.



