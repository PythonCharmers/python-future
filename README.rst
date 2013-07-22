
future: support Python 2 with fewer warts
=========================================

The ``future`` module helps run Python 3.x-compatible code under Python 2.

The goal of the ``future`` module is to allow you to write clean, modern Python
3.x-compatible code today and to run it with minimal effort under Python 2
alongside a Python 2 stack of dependencies.

It is designed to be used as follows:::

    from __future__ import division, absolute_import, print_function
    from future import common_iterators, disable_obsolete_builtins
    
    # Then Python 3-compatible code, e.g.
    for i in range(10**9):
        pass
    
    class verbose_list(list):
        def append(self, item):
            print('Adding an item')
            super().append(item)    	# new simpler super() function
    
    # These raise NameErrors:
    # apply(), cmp(), coerce(), reduce(), xrange(), etc.


Other modules include:::
    
    from __future__ import unicode_literals
	from future import str_is_unicode
    
	# Which restores this identity, normally valid on Py3 and Py2, which
	# unicode_literals breaks:
    assert str('blah') is 'blah'


``future`` also contains a ``features`` module with backports of some extra
features from Python 3.x that are not essential to the porting effort, such
as these:::

    from future.features import range, super
    
	# New range object with slicing support
    for i in range(10**11)[:10]:
        pass
    
	# New simpler super() function:
    class VerboseList(list):
        def append(self, item):
            print('Adding an item')
            super().append(item)

(These features are derived from Ryan Kelly's magicsuper module and Dan
Crosta's xrange module.)


FAQ
---


:Q: Why use this approach?

:A: Here are some quotes:

- "Django’s developers have found that attempting to write Python 3 code that’s
  compatible with Python 2 is much more rewarding than the opposite."
  from https://docs.djangoproject.com/en/dev/topics/python3/

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

:Q: Does it work?

:A: Probably not.


:Q: Who is this for?

:A: 1. People who would prefer to write clean, future-proof Python
       3.3+-compatible code, but whose day-jobs require that their code run on a
       Python 2 stack.

    2. People who wish to simplify migration of their codebases to Python 3.3+,
       module by module and feature by feature.

    3. People with existing or new Python 3.3+ codebases who wish to provide
       Python 2.6 and 2.7 support easily.

    4. People who like debugging crazy exceptions.


:Q: What is the relationship between this project and ``python-modernize``?

:A: python-modernize is great, and this project is designed to complement it.
    For a project wishing to migrate to Python 3, python-modernize is useful for
    starting the process of cleaning up legacy code idioms and translating code
    into a more modern idiom: a common subset of Python 3 and Python 2 that
    should run under either platform.

    ``future`` goes further in allowing the output of ``python-modernize`` or
    hand-written Python 3 code to run with less work and and less
    backward-compatible cruft on Python 2.


:Q: What is the relationship between this project and ``six``?

:A: ``future`` is a higher-level interface that builds on the ``six`` module.
	They share the same goal of supporting codebases that work on both Python 2
	and Python 3 without modification. They differ in the interface they offer,
	the Python versions they target, and the amount of magic in the
	implementation.
    
    Codebases that use it are sometimes standard Python 3 code, sometimes
    Python 2 code, and sometimes six-specific wrapper interfaces.
    
    Here is a simple example of code compatible with both Python 2 and Python 3
    using ``six``::
    
        from six.moves import xrange
        for i in xrange(10**8):    # invalid Python 3 code
            pass
    
    Here is the corresponding example using the ``future`` module::
    
        from future import common_iterators
        for i in range(10**8):     # standard Python 3
            pass
    
	Note that the former introduces warty Python 2 cruft into a Python 3
	codebase in order to offer Python 2 support. The latter example is standard
	Python 3 code, with an import line that has no effect on Python 3.
    
    Another difference is version support: ``future`` supports only Python 2.7
	and Python 3.3+. In contrast, six is designed to support versions of Python
	prior to 2.7 and Python 3.0-3.2. Some of the interfaces provided by six
	(like the ``next()`` function and ``from __future__ import
	print_function``) are superseded by features provided in Python 2.7.
    
	Another difference is that the implementation of ``future`` is more
	magical.


:Q: How did the original need for this arise?

:A: In teaching Python to newbies, we faced a dilemma: teach them Python 3,
	which was future-proof but not as useful today because of weaker 3rd-party
	package support, or teach them Python 2, which was more useful today but
	would require them to unlearn various habits soon. We searched for ways to
	avoid polluting the world with more deprecated code.


:Q: Do you support Pypy and/or Jython?

:A: Not sure. This would be nice. Pull requests, please!


:Q: Should I use this in production?

:A: No! Maybe one day...


:Q: Can I help?

:A: Yes, we welcome bug reports, tests, and pull requests.

