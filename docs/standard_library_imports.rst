.. _standard-library-imports:

Standard library imports
========================

:mod:`future` supports the standard library reorganization (PEP 3108). Under
the standard Python 3 names and locations, it provides access to either the
corresponding native standard library modules (``future.moves``) or to backported
modules from Python 3.3 (``future.backports``).

There are currently four interfaces to the reorganized standard library.


Context-manager interface
-------------------------
The recommended interface is via a context-manager called ``hooks``::

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
        import urllib.request
        # and other moved modules and definitions

Direct interface
----------------

The second interface avoids import hooks. It may therefore be more
robust, at the cost of less idiomatic code. Use it as follows::

    from future.moves import queue
    from future.moves import socketserver
    from future.moves.http.client import HTTPConnection
    # etc.

If you wish to achieve the effect of a two-level import such as this::

    import http.client 

portably on both Python 2 and Python 3, note that Python currently does not
support syntax like this::

    from future.moves import http.client

One workaround is to replace the dot with an underscore::

    import future.moves.http.client as http_client

import_ and from_import functions
---------------------------------

A third option, which also works with two-level imports, is to use the
``import_`` and ``from_import`` functions from ``future.standard_library`` as
follows::

    from future.standard_library import import_, from_import
    
    http = import_('http.client')
    urllib = import_('urllib.request')

    urlopen, urlsplit = from_import('urllib.request', 'urlopen', 'urlsplit')

install_hooks() call
--------------------

The fourth interface to the reorganized standard library is via an
explicit call to ``install_hooks``::

    from future import standard_library
    standard_library.install_hooks()

    import urllib
    f = urllib.request.urlopen('http://www.python.org/')

    standard_library.remove_hooks()
    standard_library.scrub_future_sys_modules()

If you use this interface, it is recommended to disable the import hooks again
after use by calling ``remove_hooks()``, in order to prevent the futurized
modules from being invoked inadvertently by other modules. (Python does not
automatically disable import hooks at the end of a module, but keeps them
active indefinitely.)

The call to ``scrub_future_sys_modules()`` removes any modules from the
``sys.modules`` cache (on Py2 only) that have Py3-style names, like ``http.client``.
This can prevent libraries that have their own Py2/3 compatibility code from
importing the ``future.moves`` or ``future.backports`` modules unintentionally.
Code such as this will then fall through to using the Py2 standard library
modules on Py2::

    try:
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection

**Requests**: The above snippet is from the `requests
<http://docs.python-requests.org>`_ library. As of v0.12, the
``future.standard_library`` import hooks are compatible with Requests.


.. If you wish to avoid changing every reference of ``http.client`` to
.. ``http_client`` in your code, an alternative is this::
.. 
..     from future.standard_library import http
..     from future.standard_library.http import client as _client
..     http.client = client

.. but it has the advantage that it can be used by automatic translation scripts such as ``futurize`` and ``pasteurize``.


List of standard library modules
--------------------------------

The modules available via ``future.moves`` are::

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
    
    import urllib
    import urllib.parse
    import urllib.request
    import urllib.error

    import xmlrpc.client
    import xmlrpc.server

..  Disabled: import test.support


Comparing future.moves and six.moves
------------------------------------

``future.moves`` and ``six.moves`` provide a similar Python 3-style
interface to the native standard library module definitions.

The major difference is that the ``future.moves`` package is a real Python package
(``future/moves/__init__.py``) with real modules provided as ``.py`` files, whereas
``six.moves`` constructs fake ``_LazyModule`` module objects within the Python
code and injects them into the ``sys.modules`` cache.

The advantage of ``six.moves`` is that the code fits in a single module that can be
copied into a project that seeks to eliminate external dependencies.

The advantage of ``future.moves`` is that it is likely to be more robust in the
face of magic like Django's auto-reloader and tools like ``py2exe`` and
``cx_freeze``. See issues #51, #53, #56, and #63 in the ``six`` project for
more detail of bugs related to the ``six.moves`` approach.


Backports
---------

Backports of the following modules from Python 3.3's standard library to Python 2.x are also
available in ``future.backports``::

    http.client
    http.server
    html.server
    urllib
    xmlrpc.client
    xmlrpc.server
 
These are currently of alpha quality. If you need the full backport of one of
these, please open an issue `here
<https://github.com/PythonCharmers/python-future>`_.

