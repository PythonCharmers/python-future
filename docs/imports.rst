.. _imports:

Imports
=======

Star imports
~~~~~~~~~~~~

If you don't mind namespace pollution on Python 2, the easiest way to provide
Py2/3 compatibility for new code using ``future`` is to include the following
imports at the top of every module::

    from __future__ import (absolute_import, division,
                            print_function, unicode_literals)
    from future.builtins import *

together with these module imports when necessary::
    
    from future import standard_library, utils

On Python 3, ``from future.builtins import *`` line has zero effect and zero
namespace pollution.

On Python 2, this import line shadows 16 builtins (listed below) to
provide their Python 3 semantics.

See :ref:`unicode-literals` for more details about this import.


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

Please note that this internal API is evolving and may not be stable
between different versions of ``future``.


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


__future__ imports
~~~~~~~~~~~~~~~~~~

For more information about the ``__future__`` imports, which are a
standard feature of Python, see the following docs:

- absolute_import: `PEP 328: Imports: Multi-Line and Absolute/Relative <http://www.python.org/dev/peps/pep-0328>`_
- division: `PEP 238: Changing the Division Operator <http://www.python.org/dev/peps/pep-0238>`_
- print_function: `PEP 3105: Make print a function <http://www.python.org/dev/peps/pep-3105>`_
- unicode_literals: `PEP 3112: Bytes literals in Python 3000 <http://www.python.org/dev/peps/pep-3112>`_

These are all available in Python 2.6 and up, and enabled by default in Python 3.x.


.. _unicode-literals:

unicode_literals
~~~~~~~~~~~~~~~~

There is some contention in the community about whether it is advisable
to import ``unicode_literals`` from ``__future__`` in a Python 2/3
compatible codebase. The ``future`` package can be used with or without
``unicode_literals`` imports, although the ``futurize`` script does imply a
preference for this by making this change at stage 2 of conversion.

To avoid confusion, we recommend using ``unicode_literals`` everywhere
across a code-base or not at all.

This section summarizes the pros and cons.

Advantages of using unicode_literals
------------------------------------

1. String literals are unicode on Python 3. Making them unicode on Python 2
   leads to more consistency of your string types the two runtimes. Most
   unintended uses of unicode strings (such as attempts to put them into
   WSGI dictionaries) will cause issues on both Python 3 and 2, making it
   more obvious where a conversion such as an ``s.encode()`` call is
   required.

2. If support for Python 3.2 is required (e.g. for Ubuntu 12.04 LTS or
   Debian wheezy), ``u''`` prefixes are a ``SyntaxError``, making
   ``unicode_literals`` the only option for a Python 2/3 compatible
   codebase.

3. Code without ``u''`` prefixes is cleaner, one of the claimed advantages
   of Python 3.

4. The diff for a Python 2 -> 2/3 port may be smaller, less noisy, and easier
   to review with ``unicode_literals`` than if an explicit ``u''`` prefix is added
   to every unadorned string literal.
  

Disadvantages of using unicode_literals
---------------------------------------

1. This is a larger-scale change than adding explicit ``u''`` prefixes to
   all strings that should be Unicode. It may introduce more regressions on
   Python 2 that require more initial investment of time to find and fix.

2. If a codebase already explicitly marks up all text with ``u''`` prefixes,
   and if support for Python versions 3.0-3.2 can be dropped, then
   removing the existing ``u''`` prefixes and replacing these with
   ``unicode_literals`` imports (the porting approach Django used) would
   introduce more noise into the patch and make it more difficult to review.
   However, note that the ``futurize`` script takes advantage of PEP 414 and
   does not remove explicit ``u''`` prefixes that already exist.

3. Turning on ``unicode_literals`` converts even docstrings to unicode, but
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


Others' perspectives
--------------------

The following `quote <https://groups.google.com/forum/#!topic/django-developers/2ddIWdicbNY>`_ is from Aymeric Augustin on 23 August 2012 regarding
why he chose ``unicode_literals`` for the port of Django to a Python
2/3-compatible codebase.

"... I'd like to explain why this PEP [PEP 414, which allows explicit
``u''`` prefixes for unicode literals on Python 3.3+] is at odds with the
porting philosophy I've applied to Django, and why I would have vetoed
taking advantage of it.

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

