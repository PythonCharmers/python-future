.. _imports:

Imports
=======

.. ___future__-imports:

__future__ imports
~~~~~~~~~~~~~~~~~~

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

Star imports
~~~~~~~~~~~~

If you don't mind namespace pollution on Python 2, the easiest way to provide
Py2/3 compatibility for new code using ``future`` is to include the following
imports at the top of every module::

    from future.builtins import *

together with these module imports when necessary::
    
    from future import standard_library, utils

On Python 3, ``from future.builtins import *`` line has zero effect and zero
namespace pollution.

On Python 2, this import line shadows 16 builtins (listed below) to
provide their Python 3 semantics.


.. _explicit-imports:

Explicit imports
~~~~~~~~~~~~~~~~

Explicit forms of the imports are often preferred and are necessary for using
some automated code-analysis tools.

The most common imports from ``future`` are::
    
    from future import standard_library, utils
    from future.builtins import (bytes, int, range, round, str, super,
                                 ascii, chr, hex, input, oct, open,
                                 filter, map, zip)

The disadvantage of importing only some of the builtins is that it
increases the risk of introducing Py2/3 portability bugs as your code
evolves over time. Be especially aware of not importing ``input``, which could
expose a security vulnerability on Python 2 if Python 3's semantics are
expected.

One further technical distinction is that unlike the ``import *`` form above,
these explicit imports do actually change ``locals()``; this is equivalent
to typing ``bytes = bytes; int = int`` etc. for each builtin.

The internal API is currently as follows::

    from future.builtins.backports import bytes, int, range, round, str, super
    from future.builtins.misc import ascii, chr, hex, input, oct, open
    from future.builtins.iterators import filter, map, zip

To understand the details of the backported builtins on Python 2, see the
docs for these modules. Please note that this internal API is evolving and may
not be stable between different versions of ``future``.


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


.. _unicode-literals:

Should I import unicode_literals?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``future`` package can be used with or without ``unicode_literals``
imports.

There is some contention in the community about whether it is advisable
to import ``unicode_literals`` from ``__future__`` in a Python 2/3
compatible codebase.

It is more compelling to use ``unicode_literals`` when back-porting
new or existing Python 3 code to Python 2/3. For porting existing Python 2
code to 2/3, explicitly marking up all unicode string literals with ``u''``
prefixes helps to avoid unintentionally changing an existing Python 2 API.

If you use ``unicode_literals``, testing and debugging your code with
*Python 3* first is probably the easiest way to fix your code. After this,
fixing Python 2 support will be easier.

To avoid confusion, we recommend using ``unicode_literals`` everywhere
across a code-base or not at all, instead of turning on for only some
modules.

This section summarizes the benefits and drawbacks of using
``unicode_literals``.

Benefits
--------

1. String literals are unicode on Python 3. Making them unicode on Python 2
   leads to more consistency of your string types across the two
   runtimes. This can make it easier to understand and debug your code.
   
2. Code without ``u''`` prefixes is cleaner, one of the claimed advantages
   of Python 3. Even though some unicode strings would require a function
   call to invert them to native strings for some Python 2 APIs (see
   :ref:`stdlib-incompatibilities`), the incidence of these function calls
   would be much lower than with using ``u''`` prefixes in the absence of
   ``unicode_literals``.

3. The diff for a Python 2 -> 2/3 port may be smaller, less noisy, and
   easier to review with ``unicode_literals`` than if an explicit ``u''``
   prefix is added to every unadorned string literal.

4. If support for Python 3.2 is required (e.g. for Ubuntu 12.04 LTS or
   Debian wheezy), ``u''`` prefixes are a ``SyntaxError``, making
   ``unicode_literals`` the only option for a Python 2/3 compatible
   codebase.


Drawbacks
---------

1. Adding ``unicode_literals`` to a module amounts to a "global flag day" for
   that module, changing the data types of all strings in the module at once.
   Cautious developers may prefer an incremental approach. (See
   `here <http://lwn.net/Articles/165039/>`_ for an excellent article
   describing the superiority of an incremental patch-set in the the case
   of the Linux kernel.)

.. This is a larger-scale change than adding explicit ``u''`` prefixes to
..  all strings that should be Unicode. 

2. Changing to ``unicode_literals`` will likely introduce regressions on
   Python 2 that require an initial investment of time to find and fix. The
   APIs may be changed in subtle ways that are not immediately obvious.

   An example on Python 2::

       ### Module: mypaths.py

       ...
       def unix_style_path(path):
           return path.replace('\\', '/')
       ...

       ### User code:

       >>> path1 = '\\Users\\Ed'
       >>> unix_style_path(path1)
       u'/Users/ed'

   On Python 2, adding a ``unicode_literals`` import to ``mypaths.py`` would
   change the return type of the ``unix_style_path`` function from ``str`` to
   ``unicode``, which is difficult to anticipate and probably unintended.
   
   The counterargument is that this code is broken, in a portability
   sense; we see this from Python 3 raising a ``TypeError`` upon passing the
   function a byte-string. The code needs to be changed to make explicit
   whether the ``path`` argument is to be a byte string or a unicode string.

3. With ``unicode_literals`` in effect, there is no way to specify a native
   string literal (``str`` type on both platforms). This can be worked around as follows::

       >>> from __future__ import unicode_literals
       >>> ...
       >>> from future.utils import bytes_to_native_str as n

       >>> s = n(b'ABCD')
       >>> s
       'ABCD'  # on both Py2 and Py3

   although this incurs a performance penalty (a function call and, on Py3,
   a ``decode`` method call.)

   This is a little awkward because various Python library APIs (standard
   and non-standard) require a native string to be passed on both Py2
   and Py3. (See :ref:`stdlib-incompatibilities` for some examples. WSGI
   dictionaries are another.)

3. If a codebase already explicitly marks up all text with ``u''`` prefixes,
   and if support for Python versions 3.0-3.2 can be dropped, then
   removing the existing ``u''`` prefixes and replacing these with
   ``unicode_literals`` imports (the porting approach Django used) would
   introduce more noise into the patch and make it more difficult to review.
   However, note that the ``futurize`` script takes advantage of PEP 414 and
   does not remove explicit ``u''`` prefixes that already exist.

4. Turning on ``unicode_literals`` converts even docstrings to unicode, but
   Pydoc breaks with unicode docstrings containing non-ASCII characters for
   Python versions < 2.7.7. (Fix committed in Jan 2014.)::

       >>> def f():
       ...     u"Author: Martin von Löwis"
       
       >>> help(f)
       
       /Users/schofield/Install/anaconda/python.app/Contents/lib/python2.7/pydoc.pyc in pipepager(text, cmd)
          1376     pipe = os.popen(cmd, 'w')
          1377     try:
       -> 1378         pipe.write(text)
          1379         pipe.close()
          1380     except IOError:
       
       UnicodeEncodeError: 'ascii' codec can't encode character u'\xf6' in position 71: ordinal not in range(128)

See `this Stack Overflow thread
<http://stackoverflow.com/questions/809796/any-gotchas-using-unicode-literals-in-python-2-6>`_
for other gotchas.


Others' perspectives
--------------------

In favour of ``unicode_literals``
*********************************

The following `quote <https://groups.google.com/forum/#!topic/django-developers/2ddIWdicbNY>`_ is from Aymeric Augustin on 23 August 2012 regarding
why he chose ``unicode_literals`` for the port of Django to a Python
2/3-compatible codebase.:

    "... I'd like to explain why this PEP [PEP 414, which allows explicit
    ``u''`` prefixes for unicode literals on Python 3.3+] is at odds with
    the porting philosophy I've applied to Django, and why I would have
    vetoed taking advantage of it.
    
    "I believe that aiming for a Python 2 codebase with Python 3
    compatibility hacks is a counter-productive way to port a project. You
    end up with all the drawbacks of Python 2 (including the legacy `u`
    prefixes) and none of the advantages Python 3 (especially the sane
    string handling).
    
    "Working to write Python 3 code, with legacy compatibility for Python
    2, is much more rewarding. Of course it takes more effort, but the
    results are much cleaner and much more maintainable. It's really about
    looking towards the future or towards the past.
    
    "I understand the reasons why PEP 414 was proposed and why it was
    accepted. It makes sense for legacy software that is minimally
    maintained. I hope nobody puts Django in this category!"


Against ``unicode_literals``
****************************

    "There are so many subtle problems that ``unicode_literals`` causes.
    For instance lots of people accidentally introduce unicode into
    filenames and that seems to work, until they are using it on a system
    where there are unicode characters in the filesystem path."

    -- Armin Ronacher
    
    "+1 from me for avoiding the unicode_literals future, as it can have
    very strange side effects in Python 2.... This is one of the key
    reasons I backed Armin's PEP 414."

    -- Nick Coghlan
    
    "Yeah, one of the nuisances of the WSGI spec is that the header values
    IIRC are the str or StringType on both py2 and py3. With
    unicode_literals this causes hard-to-spot bugs, as some WSGI servers
    might be more tolerant than others, but usually using unicode in python
    2 for WSGI headers will cause the response to fail."
    
    -- Antti Haapala


