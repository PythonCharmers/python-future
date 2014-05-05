.. _imports:

Imports
=======

.. ___future__-imports:

__future__ imports
------------------

To write a Python 2/3 compatible codebase, the first step is to add this line
to the top of each module::

    from __future__ import absolute_import, division, print_function

For guidelines about whether to import ``unicode_literals`` too, see below
(:ref:`unicode-literals`).

For more information about the ``__future__`` imports, which are a
standard feature of Python, see the following docs:

- absolute_import: `PEP 328: Imports: Multi-Line and Absolute/Relative <http://www.python.org/dev/peps/pep-0328>`_
- division: `PEP 238: Changing the Division Operator <http://www.python.org/dev/peps/pep-0238>`_
- print_function: `PEP 3105: Make print a function <http://www.python.org/dev/peps/pep-3105>`_
- unicode_literals: `PEP 3112: Bytes literals in Python 3000 <http://www.python.org/dev/peps/pep-3112>`_

These are all available in Python 2.6 and up, and enabled by default in Python 3.x.


.. _star-imports:

future imports
--------------

Implicit imports
~~~~~~~~~~~~~~~~

If you don't mind namespace pollution on Python 2, the easiest way to provide
Py2/3 compatibility for new code using ``future`` is to include the following
imports at the top of every module::

    from future.builtins import *

On Python 3, ``from future.builtins import *`` line has zero effect and zero
namespace pollution.

On Python 2, this import line shadows 18 builtins (listed below) to
provide their Python 3 semantics.


.. _explicit-imports:

Explicit imports
~~~~~~~~~~~~~~~~

Explicit forms of the imports are often preferred and are necessary for using
certain automated code-analysis tools.

The complete set of imports from ``future`` is::
    
    from future import standard_library, utils
    from future.builtins import (ascii, bytes, chr, dict, filter, hex, input,
                                 int, map, next, oct, open, pow, range, round,
                                 str, super, zip)


The disadvantage of importing only some of the builtins is that it
increases the risk of introducing Py2/3 portability bugs as your code
evolves over time. Be especially aware of not importing ``input``, which could
expose a security vulnerability on Python 2 if Python 3's semantics are
expected.

.. One further technical distinction is that unlike the ``import *`` form above,
.. these explicit imports do actually modify ``locals()`` on Py3; this is
.. equivalent to typing ``bytes = bytes; int = int`` etc. for each builtin.

The internal API is currently as follows::

    from future.types import bytes, dict, int, range, str
    from future.builtins.misc import (ascii, chr, hex, input, next,
                                      oct, open, round, super)
    from future.builtins.iterators import filter, map, zip

To understand the details of the backported builtins on Python 2, see the
docs for these modules. Please note that this internal API is evolving and may
not be stable between different versions of ``future``.


.. < Section about past.translation is included here >

.. include:: translation.rst


.. _standard-library-imports:

Standard library imports
~~~~~~~~~~~~~~~~~~~~~~~~

:mod:`future` supports the standard library reorganization (PEP 3108)
via import hooks, allowing almost all moved standard library modules to
be accessed under their Python 3 names and locations in Python 2.

There are three interfaces to the backported standard library modules. The first
is via a context-manager called ``hooks``::

    from future import standard_library
    with standard_library.hooks():
        import socketserver
        import queue
        import configparser
        import test.support
        import html.parser
        from collections import UserList
        from itertools import filterfalse, zip_longest
        from http.client import HttpConnection
        # and other moved modules and definitions

The second interface is via an explicit call to ``install_hooks``::

    from future import standard_library
    standard_library.install_hooks()

    import urllib
    f = urllib.request.urlopen('http://www.python.org/')

    standard_library.remove_hooks()

It is a good idea to disable the import hooks again after use by calling
``remove_hooks()``, in order to prevent the futurized modules from being invoked
inadvertently by other modules. (Python does not automatically disable import
hooks at the end of a module, but keeps them active indefinitely.)
    
The third interface avoids import hooks entirely. It may therefore be more
robust, at the cost of less idiomatic code. Use it as follows::

    from future.standard_library import queue
    from future.standard_library import socketserver
    from future.standard_library.http.client import HTTPConnection
    # etc.

If you wish to achieve the effect of a two-level import such as this::

    import http.client 

portably on both Python 2 and Python 3, you can use this idiom::

    from future.standard_library import http
    from future.standard_library.http import client as _client
    http.client = client

This is ugly, Python currently does not support syntax like this::

    from future.standard_library import http.client

.. but it has the advantage that it can be used by automatic translation scripts such as ``futurize`` and ``pasteurize``.


List of standard library modules
________________________________

The modules available are::

    import socketserver
    import queue
    import configparser
    from collections import UserList
    from itertools import filterfalse, zip_longest
    
    import html
    import html.entities
    import html.parser

    import http
    import http.client
    import http.server
    import http.cookies
    import http.cookiejar

..  Disabled: import test.support

The following modules are currently not supported, but we aim to support them in
the future::
    
    import urllib
    import urllib.parse
    import urllib.request
    import urllib.error

    import xmlrpc.client
    import xmlrpc.server

If you need one of these, please open an issue `here <https://github.com/PythonCharmers/python-future>`_.


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
Python 2 support, as described in :ref:`forwards-conversion-stage2`.


.. include:: unicode_literals.rst

