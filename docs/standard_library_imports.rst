.. _standard-library-imports:

Standard library imports
========================

:mod:`future` supports the standard library reorganization (PEP 3108). Under
the standard Python 3 names and locations, it provides access to either the
corresponding native standard library modules (``future.moves``) or backported
modules from Python 3.3 on Python 2 (``future.standard_library``).

There are four interfaces to the reorganized standard library. The
first is via a context-manager called ``hooks``::

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

The second interface avoids import hooks. It may therefore be more
robust, at the cost of less idiomatic code. Use it as follows::

    from future.standard_library import queue
    from future.standard_library import socketserver
    from future.standard_library.http.client import HTTPConnection
    # etc.

If you wish to achieve the effect of a two-level import such as this::

    import http.client 

portably on both Python 2 and Python 3, note that Python currently does not
support syntax like this::

    from future.standard_library import http.client

One workaround (which ``six.moves`` also requires) is to replace the dot with
an underscore::

    import future.standard_library.http.client as http_client

The other workaround is to use the ``import_`` and ``from_import`` functions as
follows::

    from future.standard_library import import_, from_import
    
    http = import_('http.client')
    urllib = import_('urllib.request')

    urlopen, urlsplit = from_import('urllib.request', 'urlopen', 'urlsplit')


The third (deprecated) interface to the reorganized standard library is via an
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
importing the ``future.standard_library`` modules unintentionally. Code such as
this will then fall through to using the Py2 standard library
modules on Py2::

    try:
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection

**Requests**: The above snippet is from the `requests
<http://docs.python-requests.org>`_ library. Note that ``requests``  is
currently incompatible with the import hooks in ``future.standard_library``. To
use both of these together, you must call ``remove_hooks()`` and
``scrub_future_sys_modules()`` as above before you (or users of your library)
import ``requests``. The easiest way to do this is with the ``hooks`` context
manager or one of the other import mechanisms (see above).


.. If you wish to avoid changing every reference of ``http.client`` to
.. ``http_client`` in your code, an alternative is this::
.. 
..     from future.standard_library import http
..     from future.standard_library.http import client as _client
..     http.client = client

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

Backports of the following modules are currently not supported, but we aim to support them in
the future::
    
    import urllib
    import urllib.parse
    import urllib.request
    import urllib.error

    import xmlrpc.client
    import xmlrpc.server

If you need one of these, please open an issue `here <https://github.com/PythonCharmers/python-future>`_.

