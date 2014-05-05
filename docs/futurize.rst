.. _forwards-conversion:

Futurize: 2 to both
--------------------

For example, running ``futurize`` turns this Python 2 code::
    
    import ConfigParser                 # Py2 module name

    class Upper(object):
        def __init__(self, iterable):
            self._iter = iter(iterable)
        def next(self):                 # Py2-style iterator interface
            return next(self._iter).upper()
        def __iter__(self):
            return self

    itr = Upper('hello')
    print next(itr),
    for letter in itr:
        print letter,                   # Py2-style print statement

into this code which runs on both Py2 and Py3::
    
    from __future__ import print_function
    from future import standard_library
    standard_library.install_hooks()
    from future.builtins import next
    from future.builtins import object
    import configparser                 # Py3-style import

    class Upper(object):
        def __init__(self, iterable):
            self._iter = iter(iterable)
        def __next__(self):             # Py3-style iterator interface
            return next(self._iter).upper()
        def __iter__(self):
            return self

    itr = Upper('hello')
    print(next(itr), end=' ')           # Py3-style print function
    for letter in itr:
        print(letter, end=' ')


To write out all the changes to your Python files that ``futurize`` suggests,
use the ``-w`` flag.

For complex projects, it is probably best to divide the porting into two stages.
Stage 1 is for "safe" changes that modernize the code but do not break Python
2.6 compatibility or introduce a depdendency on the ``future`` package. Stage 2
is to complete the process.


.. _forwards-conversion-stage1:

Stage 1: "safe" fixes
~~~~~~~~~~~~~~~~~~~~~

Run the first stage of the conversion process with::

	futurize --stage1 mypackage/*.py

or, if you are using zsh, recursively::

    futurize --stage1 mypackage/**/*.py

This applies fixes that modernize Python 2 code without changing the effect of
the code. With luck, this will not introduce any bugs into the code, or will at
least be trivial to fix. The changes are those that bring the Python code
up-to-date without breaking Py2 compatibility. The resulting code will be
modern Python 2.6-compatible code plus ``__future__`` imports from the
following set::

    from __future__ import absolute_import
    from __future__ import division
    from __future__ import print_function

Only those ``__future__`` imports deemed necessary will be added unless
the ``--all-imports`` command-line option is passed to ``futurize``, in
which case they are all added.

The ``from __future__ import unicode_literals`` declaration is not added
unless the ``--unicode-literals`` flag is passed to ``futurize``.

The changes include::

    - except MyException, e:
    + except MyException as e:

    - print >>stderr, "Blah"
    + from __future__ import print_function
    + print("Blah", stderr)

    - class MyClass:
    + class MyClass(object):

    - def next(self):
    + def __next__(self):

    - if d.has_key(key):
    + if key in d:

Implicit relative imports fixed, e.g.::

    - import mymodule
    + from __future__ import absolute_import
    + from . import mymodule

.. and all unprefixed string literals '...' gain a b prefix to be b'...'.

.. (This last step can be prevented using --no-bytes-literals if you already have b'...' markup in your code, whose meaning would otherwise be lost.)

Stage 1 does not add any imports from the ``future`` package. The output of
stage 1 will probably not (yet) run on Python 3. 

The goal for this stage is to create most of the ``diff`` for the entire
porting process, but without introducing any bugs. It should be uncontroversial
and safe to apply to every Python 2 package. The subsequent patches introducing
Python 3 compatibility should then be shorter and easier to review.

The complete set of fixers applied by ``futurize --stage1`` is::

    lib2to3.fixes.fix_apply
    lib2to3.fixes.fix_except
    lib2to3.fixes.fix_exitfunc
    lib2to3.fixes.fix_funcattrs
    lib2to3.fixes.fix_has_key
    lib2to3.fixes.fix_idioms
    lib2to3.fixes.fix_intern
    lib2to3.fixes.fix_isinstance
    lib2to3.fixes.fix_methodattrs
    lib2to3.fixes.fix_ne
    lib2to3.fixes.fix_next
    lib2to3.fixes.fix_numliterals
    lib2to3.fixes.fix_paren
    lib2to3.fixes.fix_reduce
    lib2to3.fixes.fix_renames
    lib2to3.fixes.fix_repr
    lib2to3.fixes.fix_standarderror
    lib2to3.fixes.fix_sys_exc
    lib2to3.fixes.fix_throw
    lib2to3.fixes.fix_tuple_params
    lib2to3.fixes.fix_types
    lib2to3.fixes.fix_ws_comma
    lib2to3.fixes.fix_xreadlines
    libfuturize.fixes.fix_absolute_import
    libfuturize.fixes.fix_division
    libfuturize.fixes.fix_print_with_import
    libfuturize.fixes.fix_raise
    libfuturize.fixes.fix_order___future__imports


.. _forwards-conversion-stage2:

Stage 2: Py3-style code with ``future`` wrappers for Py2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run stage 2 of the conversion process with::

    futurize —-stage2 myfolder/*.py

This stage adds a dependency on the ``future`` package. The goal for stage 2 is
to make further mostly safe changes to the Python 2 code to use Python 3-style
code that then still runs on Python 2 with the help of the appropriate builtins
and utilities in ``future``.

For example::

    name = raw_input('What is your name?\n')

    for k, v in d.iteritems():
        assert isinstance(v, basestring)

    class MyClass(object):
        def __unicode__(self):
            return u'My object'
        def __str__(self):
            return unicode(self).encode('utf-8')

would be converted by Stage 2 to this code::

    from future.builtins import input
    from future.builtins import str
    from future.utils import iteritems, python_2_unicode_compatible

    name = input('What is your name?\n')

    for k, v in iteritems(d):
        assert isinstance(v, (str, bytes))

    @python_2_unicode_compatible
    class MyClass(object):
        def __str__(self):
            return u'My object'

Stage 2 also renames standard-library imports to their Py3 names and adds these
two lines::

    from future import standard_library
    standard_library.install_hooks()

For example::

    import ConfigParser

becomes::
    
    from future import standard_library
    standard_library.install_hooks()
    import configparser


.. Ideally the output of this stage should not be a ``SyntaxError`` on either
.. Python 3 or Python 2.

.. _forwards-conversion-text:

Separating text from bytes
~~~~~~~~~~~~~~~~~~~~~~~~~~

After applying stage 2, the recommended step is to decide which of your Python
2 strings represent text and which represent binary data and to prefix all
string literals with either ``b`` or ``u`` accordingly. Furthermore, to ensure
that these types behave similarly on Python 2 as on Python 3, also wrap
byte-strings or text in the ``bytes`` and ``str`` types from ``future``. For
example::
    
    from future.builtins import bytes, str
    b = bytes(b'\x00ABCD')
    s = str(u'This is normal text')

Any unadorned string literals will then represent native platform strings
(byte-strings on Py2, unicode strings on Py3).

An alternative is to pass the ``--unicode_literals`` flag::
  
  $ futurize --unicode_literals mypython2script.py

After running this, all string literals that were not explicitly marked up as
``b''`` will mean text (Python 3 ``str`` or Python 2 ``unicode``).



.. _forwards-conversion-stage3:

Post-conversion
~~~~~~~~~~~~~~~

After running ``futurize``, we recommend first running your tests on Python 3 and making further code changes until they pass on Python 3. 

The next step would be manually tweaking the code to re-enable Python 2
compatibility with the help of the ``future`` package. For example, you can add
the ``@python_2_unicode_compatible`` decorator to any classes that define custom
``__str__`` methods. See :ref:`what-else` for more info.


