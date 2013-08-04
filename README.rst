future: clean single-source support for Python 3 and 2
======================================================

The ``future`` module helps run Python 3.x-compatible code under Python 2
with minimal code cruft.

The goal is to allow you to write clean, modern, forward-compatible
Python 3 code today and to run it with minimal effort under Python 2
alongside a Python 2 stack that may contain dependencies that have not
yet been ported to Python 3.

It is designed to be used as follows::

    from __future__ import (division, absolute_import, print_function,
                            unicode_literals)
    from future import *
    
followed by clean Python 3 code (with a few restrictions) that can run
unchanged on Python 2.7.

On Python 3, the ``from future import *`` line has no effect (i.e. zero
namespace pollution.) On Python 2 it shadows builtins to provide the
Python 3 semantics. (See below for the explicit import form.)

After the imports, this code runs identically on Python 3 and 2::
    
    # New iterable range object with slicing support
    for i in range(10**11)[:10]:
        pass
    
    # Other common iterators: map, reduce, zip
    my_iter = zip(range(3), ['a', 'b', 'c'])
    assert my_iter != list(my_iter)
    
    # New simpler super() function:
    class VerboseList(list):
        def append(self, item):
            print('Adding an item')
            super().append(item)
    
    # These raise NameErrors:
    # apply(), cmp(), coerce(), reduce(), xrange(), etc.
    
    # This identity is restored. This is normally valid on Py3 and Py2, but
    # 'from __future__ import unicode_literals' breaks it on Py2:
    assert isinstance('happy', str)
    
    # The round() function behaves as it does in Python 3, using "Banker's
    # Rounding" to the nearest even last digit:
    assert round(0.1250, 2) == 0.12
    
    # input() is now safe (no eval()):
    name = input('What is your name? ')
    print('Hello ' + name)


``future`` also supports the standard library reorganization (PEP 3108)
via import hooks, allowing standard library modules to be accessed under
their Python 3 names and locations::
    
    from future import standard_library
    
    import socketserver
    import queue
    import configparser
    import test.support
    from collections import UserList
    from itertools import filterfalse
    # and other moved modules and definitions

It also includes backports for three stdlib packages from Py3 that were
heavily refactored versus Py2::
    
    import html, html.entities, html.parser
    import http, http.client

These currently are not supported, but we may support them in the
future::
    
    import http.server, http.cookies, http.cookiejar
    import urllib, urllib.parse, urllib.request, urllib.error


Explicit imports
----------------
If you prefer explicit imports, the explicit equivalent of the ``from
future import *`` line above is::
    
    from future.common_iterators import zip, map, filter
    from future.builtins import ascii, oct, hex, chr
    from future.modified_builtins import (range, super, round, input)
    from future.disable_obsolete_builtins import (apply, cmp, coerce,
            execfile, file, long, raw_input, reduce, reload, unicode,
            xrange, StandardError)
    from future.str_is_unicode import str

But please note that the API is still evolving rapidly.

See the docstrings for each of these modules for more info::

- future.standard_library
- future.common_iterators
- future.builtins
- future.modified_builtins
- future.disable_obsolete_builtins
- future.str_as_unicode


Automatic conversion
====================

There is a script included called ``futurize.py`` to aid in making either
Python 2 code or Python 3 code compatible with both platforms using the
``future`` module. It is based on 2to3 and inspired by Armin Ronacher's
``modernize.py``.

For Python 2 code (the default), it runs the code through all the
appropriate 2to3 fixers to turn it into valid Python 3 code, and then
adds ``__future__`` and ``future`` package imports so that (hopefully)
the resulting code runs on Python 3 as well.

For Python 3 code (with ``--from3``), it merely adds ``__future__`` and
``future`` imports to the top of each module so that (with luck) the code
will run automatically on Python 2 as well.


Limitations
-----------
Python 3 code that causes SyntaxErrors on Python 2 is not currently
handled by the ``futurize`` script (except for ``print_function``). This
includes:

- Function arguments in Py3.3 like this::
    ``def f(a, b, *, c='blah', d='blah'):``
        ``pass``

- ``yield ... from`` syntax for generators in Py3.3

- ``raise ... from`` syntax for exceptions. (This is simple to fix
  manually by creating a temporary variable.)

- And any code that requires new standard library features from Python 3
  that weren't present under Python 2.

- ``class MyClass:``
      ``...``

  should be changed back to:
  
  ``class MyClass(object):``
      ``...``

  to get new-style classes; otherwise weird breakage when e.g. calling
  super() may occur. Currently futurize.py doesn't do this automatically.


Credits
-------
:Author:  Ed Schofield
:Sponsor: Python Charmers Pty Ltd, Australia, and Python Charmers Pte
          Ltd, Singapore. http://pythoncharmers.com
:Others:  The ``super()`` and ``range()`` functions are derived from Ryan
          Kelly's ``magicsuper`` module and Dan Crosta's ``xrange``
          module. The ``python_2_unicode_compatible`` decorator is from
          ``django.utils.encoding``. The ``fix_metaclass`` 2to3 fixer
          (from Armin Ronacher's ``python-modernize``) was authored by
          Jack Diederich and Daniel Neuhaeuser.


Licensing
---------
Copyright 2013 Python Charmers Pty Ltd, Australia.
The software is distributed under an MIT licence. See LICENSE.txt.


FAQ
===
:Q: Why use this approach?

:A: Here are some quotes:

- "Django's developers have found that attempting to write Python 3 code
  that's compatible with Python 2 is much more rewarding than the
  opposite." from https://docs.djangoproject.com/en/dev/topics/python3/

- "Thanks to Python 3 being more strict about things than Python 2 (e.g., bytes
  vs. strings), the source translation [from Python 3 to 2] can be easier and
  more straightforward than from Python 2 to 3. Plus it gives you more direct
  experience developing in Python 3 which, since it is the future of Python, is
  a good thing long-term."
  from the official guide "Porting Python 2 Code to Python 3" by Brett Cannon:
  http://docs.python.org/2/howto/pyporting.html

- "Developer energy should be reserved for addressing real technical
  difficulties associated with the Python 3 transition (like distinguishing
  their 8-bit text strings from their binary data). They shouldn't be punished
  with additional code changes (even automated ones) ..."
  also PEP 414: from http://www.python.org/dev/peps/pep-0414/


:Q: Who is this for?

:A: 1. People who would prefer to write clean, future-proof Python
       3-compatible code, but whose day-jobs require that their code run on a
       Python 2 stack.

    2. People who wish to simplify migration of their codebases to Python 3.3+,
       module by module and feature by feature.

    3. People with existing or new Python 3 codebases who wish to provide
       Python 2.7 support easily.


:Q: Why is there a need for this?

:A: "Python 2 is the next COBOL." - Alex Gaynor, at PyCon AU 2013

    Python 2.7 is the end of the Python 2 line. The language and standard
    libraries are improving only in Python 3.x. Python 3.3 is a better
    language and better set of standard libraries than Python 2.x in
    almost every way.

    ``future`` helps you to take advantage of the cleaner semantics of
    Python 3 code today while still supporting Python 2. The goal is to
    facilitate writing future-proof code and give the Python community an
    easier upgrade path to Python 3.
    

Other compatibility tools
-------------------------

:Q: What is the relationship between this project and ``2to3``?

:A: ``2to3`` is a powerful and flexible tool that can produce different
    styles of Python 3 code. It is, however, primarily designed for
    one-way porting efforts, for projects that can leave behind Python 2
    support.

    The example at the top of the 2to3 docs
    (http://docs.python.org/2/library/2to3.html) illustrates this point.
    After transformation, ``example.py`` looks like this::

        def greet(name):
            print("Hello, {0}!".format(name))
        print("What's your name?")
        name = input()
        greet(name)

    This is Python 3 code that, although syntactically valid on Python 2,
    is actually semantically incorrect. On Python 2, it raises an
    exception for most inputs; worse, it allows arbitrary code execution
    by the user for specially crafted inputs.

    Almost every output of ``2to3`` will need modification to provide
    backward compatibility with Python 2. ``future`` is designed for just
    this purpose.


:Q: Can't I maintain a Python 2 codebase and use 2to3 to automatically
    convert to Python 3 in the setup script?

:A: Yes, this is possible, but then your actual working codebase will be
    stuck with only Python 2's features (and its warts) for as long as you
    need to retain Python 2 compatibility. This may be at least 5 years
    for many projects.

    This approach also carries the significant disadvantage that you
    cannot apply patches submitted by Python 3 users against the
    auto-generated Python 3 code. (See
    http://www.youtube.com/watch?v=xNZ4OVO2Z_E.)


:Q: What is the relationship between this project and ``six``?

:A: ``future`` is a higher-level interface that incorporates the ``six``
    module.  They share the same goal of making it possible to write a
    single-source codebase that works
    on both Python 2 and Python 3 without modification. ``future`` offers
    a cleaner interface that works with standard Python 3 code and
    supports more new Python 3 features.
    
    Codebases that use ``six`` directly tend to be mixtures of
    Python 2 code, Python 3 code, and ``six``-specific wrapper
    interfaces. In practice it sometimes looks like this::
    
        from sklearn.externals.six.moves import (cStringIO as StringIO,
                                                 xrange)

        for i, (k, v) in enumerate(sorted(six.iteritems(params))):
            # ...

        if six.PY3:
            exec(open('setup.py').read(), {'__name__'='__main__'})
        else:
            execfile('setup.py', {'__name__'='__main__'})
        
        for i in xrange(n):          # non-standard Python 3
            pass
    

    Such a mixture of interfaces puts a maintenance burden on the code to
    support both versions.

    Here is the equivalent code using the ``future`` module::
    
        from future import standard_library, range

        for i, (k, v) in enumerate(sorted(params.items())):
            # ...

        exec(open('setup.py').read(), {'__name__'='__main__'})
        
        for i in range(n):           # standard Python 3
            pass
    
    This is standard Python 3 code, with an import line that
    has no effect on Python 3.
    
    Another difference is version support: ``future`` supports only
    Python 2.7 and Python 3.2+. In contrast, six is designed to support
    versions of Python prior to 2.7 and Python 3.0-3.1. Some of the
    interfaces provided by six (like the ``next()`` and ``print_()``
    functions) are superseded by features introduced in Python 2.6 or
    2.7.

    The final difference is in scope: ``future`` offers more backported
    features from Python 3, including the improved no-argument super()
    function, the new range object (with slicing support), rounding
    behaviour, and some backported stdlib modules such as ``urllib``.
    More backported features will be added in the future. This should
    reduce the burden on every project to roll its own py3k compatibility
    wrapper module.

:Q: What is the relationship between this project and ``python-modernize``?

:A: ``python-modernize`` converts legacy code into what is (hopefully) a
    common subset of Python 2 and 3, with ``six`` as a run-time dependency. 

    ``python-future`` contains a ``futurize.py`` script that is similar
    to ``modernize.py`` in intent and design (based on ``2to3``). The
    difference is that ``futurize`` produces code that is
    source-compatible with Py2 and Py3 by using ``future`` package
    imports, rather than ``six``.

:Q: How did the original need for this arise?

:A: In teaching Python, we at Python Charmers faced a dilemma: teach
    people Python 3, which was future-proof but not as useful to them because
    of weaker 3rd-party package support, or teach them Python 2, which was
    more useful today but would require people to change their code and
    unlearn various habits soon. We searched for ways to avoid polluting the
    world with more deprecated code, but didn't find a good way.

    Also, in attempting to port ``scikit-learn`` to Python 3, I (Ed) was
    dissatisfied with how much code cruft was necessary to introduce to
    support Python 2 and 3 from a single codebase (the preferred porting
    option). 
    
    Since backward-compatibility with Python 2 may be necessary
    for at least the next 5 years, one of the promised benefits of Python
    3 -- cleaner code with fewer of Python 2's warts -- was difficult to
    realise before in practice in a single codebase that supported both
    platforms.


:Q: Do you support Pypy?

:A: Yes, except for the standard_library feature (currently).
    Feedback and pull requests are welcome!

:Q: Do you support IronPython and/or Jython?

:A: Not sure. This would be nice.


:Q: Can I help?

:A: Yes please :) I welcome bug reports, tests, and pull requests.


