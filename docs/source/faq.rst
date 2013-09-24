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
  with additional code changes ..."
  also PEP 414: from http://www.python.org/dev/peps/pep-0414/

- "Duplication of effort is wasteful, and replacing the various
  home-grown approaches with a standard feature usually ends up making
  things more readable, and interoperable as well." -- Guido van Rossum,
  from http://www.artima.com/weblogs/viewpost.jsp?thread=86641.


:Q: Who is this for?

:A: 1. People who would prefer to write clean, future-proof Python
       3-compatible code, but whose day-jobs require that their code run on a
       Python 2 stack.

    2. People who wish to simplify migration of their codebases to Python 3.3+,
       module by module and feature by feature.

    3. People with existing or new Python 3 codebases who wish to provide
       ongoing Python 2.7 support easily and with little maintenance burden.

    4. Package authors who want to reduce bugs with porting by not
       having to write their own home-grown Python 2/3 compatibility
       modules.


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
    

:Q: Are there any example of Python 2 packages ported to Python 3 using
``future`` and ``futurize``?

:A: Yes, an example is the port of ``xlwt``, available here::

- https://github.com/python-excel/xlwt/pull/32

The code also contains backports for several Py3 standard library modules
under ``future/standard_library/``.


Other compatibility tools
-------------------------

:Q: What is the relationship between this project, ``2to3``, and
    ``lib2to3``?

:A: ``2to3`` is a powerful and flexible tool that can produce different
    styles of Python 3 code. It is, however, primarily designed for
    one-way porting efforts, for projects that can leave behind Python 2
    support.

    The example at the top of the ``2to3`` docs
    (http://docs.python.org/2/library/2to3.html) demonstrates this.
    After transformation by ``2to3``, ``example.py`` looks like this::

        def greet(name):
            print("Hello, {0}!".format(name))
        print("What's your name?")
        name = input()
        greet(name)

    This is Python 3 code that, although syntactically valid on Python 2,
    is semantically incorrect. On Python 2, it raises an exception for
    most inputs; worse, it allows arbitrary code execution by the user
    for specially crafted inputs because of the ``eval()`` executed by Python
    2's ``input()`` function.

    This is not an isolated example; almost every output of ``2to3`` will
    need modification to provide backward compatibility with Python 2.
    ``future`` is designed for just this purpose.

    ``future`` contains a script called ``futurize`` that is based on
    ``lib2to3`` and ``lib3to2`` and a select set of their fixers.
    ``futurize`` is designed to turn Python 2 (or Python 3) code into
    code that is compatible with both platforms.


:Q: Can't I maintain a Python 2 codebase and use 2to3 to automatically
    convert to Python 3 in the setup script?

:A: Yes, this is possible, and was originally the approach recommended by
    Python's core developers, but has some large drawbacks.
    
    First, your actual working codebase will be stuck with only Python
    2's features, and its warts, for as long as you need to retain Python
    2 compatibility. This may be at least 5 years for many projects.
    
    This approach also carries the significant disadvantage that you
    cannot apply patches submitted by Python 3 users against the
    auto-generated Python 3 code. (See
    http://www.youtube.com/watch?v=xNZ4OVO2Z_E.)


:Q: What is the relationship between this project and ``six``?

:A:	``future`` is a higher-level compatibility layer that incorporates Benjamin
	Peterson's ``six`` module (available as ``future.utils.six``), as well as
	additional backported functionality from Python 3.
	
    ``future`` and ``six`` share the same goal of making it possible to write a
	single-source codebase that works on both Python 2 and Python 3.
	``future`` has the further goal of allowing standard Py3 code to run with
	almost no modification on both Py3 and Py2. It provides a more complete set
	of support for Python 3's features, including backports of the Python 3
	``bytes`` object (which is very different to Python 2's ``str`` object) and
	several standard library modules.

	There is a difference in version support: ``future`` supports only Python
	2.7 and Python 3.3+, whereas ``six`` supports all versions of Python from
	2.4 onwards. Because of this, ``future`` is able to offer a cleaner
	interface that leverages some important backward-compatibility features
	introduced into Python 2.6 and 2.7. In comparison, code using ``six``
	directly tends to be unidiomatic, with a mix of Py2, Py3 and
	``six``-specific conventions, which carries a higher maintenance burden on
	code than clean Python 3 code using ``future``.

	There is also a difference in scope: ``future`` offers a more complete set of backported
	builtins and standard library modules, as well as various Py2/3 compatibility
	tools picked from successful projects, which should hopefully reduce the
	burden on every project to roll its own py3k compatibility wrapper module.

:Q: What is the relationship between this project and ``python-modernize``?

:A: ``python-future`` contains, in addition to the ``future``
    compatibility package, a ``futurize`` script that is similar to
	``python-modernize.py`` in intent and design. Both are based heavily on
	``2to3``.
    
    Whereas ``python-modernize`` converts Py2 code into a common
    subset of Python 2 and 3, with ``six`` as a run-time dependency,
	``futurize`` converts either Py2 or Py3 code into (almost) standard Python
	3 code, with ``future`` as a run-time dependency.    

    Because ``future`` incorporates ``six`` and also provides more
    backported Py3 behaviours, the code resulting from ``futurize``
    should be cleaner and require less additional manual porting effort
    to handle renamed modules and modified builtins.

:Q: How did the original need for this arise?

:A: In teaching Python, we at Python Charmers faced a dilemma: teach
    people Python 3, which was future-proof but not as useful to them because
    of weaker 3rd-party package support, or teach them Python 2, which was
    more useful today but would require people to change their code and
    unlearn various habits soon. We searched for ways to avoid polluting the
    world with more deprecated code, but didn't find a good way.

    Also, in attempting to port packages such as ``scikit-learn`` to Python 3,
    I (Ed) was dissatisfied with how much code cruft was necessary to introduce
    to support Python 2 and 3 from a single codebase (the preferred porting
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

