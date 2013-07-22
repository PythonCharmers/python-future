
future: support Python 2 with fewer warts
=========================================

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
unchanged on Python 2.7 or Python 3.3. For example::

    # New range object with slicing support
    for i in range(10**11)[:10]:
        pass
    
    # Other common iterators: map, reduce, zip
    iter = zip(range(3), ['a', 'b', 'c'])
    assert iter != list(iter)
    
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
    
See below for more explicit forms of the import line.
    
Another feature offered is support for the standard library
reorganization (PEP 3108)::
    
    from future import standard_library_renames
    
    import socketserver
    import queue
    import configparser
    # etc.

and other modules renamed for Python 3.

The above * import is equivalent to::
    
    from future.common_iterators import zip, map, filter
    from future.features import range, super
    from future.disable_obsolete_builtins import (apply, cmp, coerce,
            execfile, file, long, raw_input, reduce, reload, unicode,
            xrange, StandardError)
    from future.str_is_unicode import str, python_2_unicode_compatible


See the docstrings for each of these modules for more info::
    
- future.standard_library_renames
- future.common_iterators
- future.features
- future.disable_obsolete_builtins
- future.str_as_unicode


Credits
-------
:Author: Ed Schofield
:Sponsor: Python Charmers Pty Ltd, Australia, and Python Charmers Pte
          Ltd, Singapore. http://pythoncharmers.com
:Others: The ``super()`` and ``range()`` functions are derived from Ryan Kelly's
         ``magicsuper`` module and Dan Crosta's ``xrange`` module. The
         ``python_2_unicode_compatible decorator`` is from
         ``django.utils.encoding``


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
       3.3+-compatible code, but whose day-jobs require that their code run on a
       Python 2 stack.

    2. People who wish to simplify migration of their codebases to Python 3.3+,
       module by module and feature by feature.

    3. People with existing or new Python 3.3+ codebases who wish to provide
       Python 2.6 and 2.7 support easily.


:Q: Why is there a need for this?

:A: To reduce cruft in single-source codebases that support both Python 2
    and 3.


Other compatibility tools
-------------------------

:Q: What is the relationship between this project and ``2to3``?

:A: ``2to3`` is a powerful and flexible tool that can produce different
    styles of Python 3 code. It is, however, primarily designed for
    one-way porting efforts, for projects that can leave behind Python 2
    support.

    The example at the top of the 2to3 docs
    (http://docs.python.org/2/library/2to3.html) illustrates this point.
    After transformation, ``example.py`` looks like this:

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


:Q: What is the relationship between this project and ``python-modernize``?

:A: ``python-modernize`` is great, and this project is designed to
    complement it.  For a project wishing to migrate to Python 3,
    python-modernize is useful for starting the process of cleaning up
    legacy code idioms which would cause SyntaxErrors on Python 3. The
    output of ``python-modernize`` should hopefully be a valid common
    subset of Python 3 and Python 2 that should run under either
    platform.

    However, the output of ``python-modernize`` is not clean Python 3
    code; it requires that code contain various backward-compatibility
    warts and a runtime dependency on the six module.
    
    ``future`` goes further in allowing either the output of
    ``python-modernize`` or hand-written Python 3 code to run with less
    work and and less backward-compatible cruft on Python 2.


:Q: What is the relationship between this project and ``six``?

:A: ``future`` is a higher-level interface that incorporates the ``six``
    module.  They share the same goal of supporting codebases that work
    on both Python 2 and Python 3 without modification. They differ in
    the interface they offer, the Python versions they target, and the
    extent of the support they offer for new Python 3 features.
    
    Codebases that use ``six`` are sometimes standard Python 3 code,
    sometimes Python 2 code, and sometimes neither (``six``-specific
    wrapper interfaces).
    
    Here is a simple example of code compatible with both Python 2 and
    Python 3 using ``six``::
    
        from six.moves import xrange
        for i in xrange(10**10):    # non-standard Python 3 code
            pass
    
    Here is the corresponding example using the ``future`` module::
    
        from future.features import range
        for i in range(10**10):     # standard Python 3
            pass
    
    Note that the former introduces the obsolete xrange() back into the
    codebase in order to offer backward compatibility for Python 2. The
    latter example is standard Python 3 code, with an import line that
    has no effect on Python 3.
    
    Another difference is version support: ``future`` supports only
    Python 2.7 and Python 3.3+. In contrast, six is designed to support
    versions of Python prior to 2.7 and Python 3.0-3.2. Some of the
    interfaces provided by six (like the ``next()`` and ``print_()``
    functions) are superseded by features introduced in Python 2.6 or
    2.7.

    The final difference is that ``future`` offers some backported features
    from Python 3, including the improved no-argument super() function,
    and the new range object (with slicing support). More backported
    features will be added in the future.


:Q: How did the original need for this arise?

:A: In teaching Python, we faced a dilemma: teach people Python 3, which
    was future-proof but not as useful to them because of weaker 3rd-party
    package support, or teach them Python 2, which was more useful today but
    would require people to change their code and unlearn various habits
    soon. We searched for ways to avoid polluting the world with more
    deprecated code, but didn't find a good way.

    Also, in attempting to port ``scikit-learn`` to Python 3, I (Ed) was
    dissatisfied with how much code cruft was necessary to introduce to
    support Python 2 and 3 from a single codebase (the preferred porting
    option). 
    
    Since backward-compatibility with Python 2 may be necessary
    for at least the next 5 years, one of the promised benefits of Python
    3 -- cleaner code with fewer of Python 2's warts -- was difficult to
    realise before in practice in a single codebase that supported both
    versions.


:Q: Do you support Pypy?

:A: Yes, except for the standard_library_renames feature (currently).
    Feedback and pull requests are welcome!

:Q: Do you support IronPython and/or Jython?

:A: Not sure. This would be nice.


:Q: Can I help?

:A: Yes, we welcome bug reports, tests, and pull requests.


