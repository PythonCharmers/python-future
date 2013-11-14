.. _automatic-conversion:

Automatic conversion with ``futurize``
======================================

The ``future`` source tree includes an experimental script called
``futurize`` to aid in making either Python 2 code or Python 3 code
compatible with both platforms using the :mod:`future` module. It is
based on 2to3 and uses fixers from ``lib2to3``, ``lib3to2``, and
``python-modernize``.

For Python 2 code (the default), it runs the code through all the
appropriate 2to3 fixers to turn it into valid Python 3 code, and then
adds ``__future__`` and ``future`` package imports. For Python 3 code
(with the ``--from3`` command-line option), it fixes Py3-only syntax
(e.g.  metaclasses) and adds ``__future__`` and ``future`` imports to the
top of each module. In both cases, the result should be relatively clean
Py3-style code semantics that (hopefully) runs unchanged on both Python 2
and Python 3.

.. _forwards-conversion:

Forwards: 2 to both
--------------------

For example, running ``futurize`` turns this Python 2 code::
    
    import ConfigParser

    class Blah(object):
        pass
    print 'Hello',

into this code which runs on both Py2 and Py3::
    
    from __future__ import print_function
    from future import standard_library
    
    import configparser

    class Blah(object):
        pass
    print('Hello', end=' ')


To write out all the changes to your Python files that ``futurize`` suggests, use the ``-w`` flag.

For complex projects, it may be better to divide the porting into two stages. Stage 1 is for "safe" changes that modernize the code but do not break Python 2.6 compatibility or introduce a depdendency on the ``future`` package. Stage 2 is to complete the process.


.. _forwards-conversion-stage1:

Stage 1: "safe" fixes
~~~~~~~~~~~~~~~~~~~~~

Run with::

	futurize --stage1

This applies fixes that modernize Python 2 code without changing the effect of
the code. With luck, this will not introduce any bugs into the code. The
changes are those that bring the Python code up-to-date without breaking Py2
compatibility. The resulting code will be perfectly good Python 2.x code plus
``__future__`` imports from the following set::

    from __future__ import absolute_import
    from __future__ import division
    from __future__ import print_function

Only those ``__future__`` imports deemed necessary will be added unless
the ``--all-imports`` command-line option is passed to ``futurize``, in
which case they are all added.

The changes include::

    - except MyException, e:
    + except MyException as e:
    
    - print >>stderr, "Blah"
    + from __future__ import print_function
    + print("Blah", stderr)

Implicit relative imports fixed, e.g.::

    - import mymodule
    + from __future__ import absolute_import
    + from . import mymodule

The ``from __future__ import unicode_literals`` declaration is not yet added
during stage 1.

.. and all unprefixed string literals '...' gain a b prefix to be b'...'.

.. (This last step can be prevented using --no-bytes-literals if you already have b'...' markup in your code, whose meaning would otherwise be lost.)

Stage 1 does not add any ``future`` imports. The output of stage 1 will
probably not (yet) run on Python 3. 

The idea is that this stage will create the majority of the lines in the
``diff`` for the entire porting process, but without introducing any bugs. It
should be uncontroversial and safe to apply to every Python 2 package. The
subsequent patches introducing Python 3 compatibility should then be shorter
and easier to review.


.. _forwards-conversion-text:

Separating text from bytes
~~~~~~~~~~~~~~~~~~~~~~~~~~

After applying stage 1, the recommended step is to decide which of your Python
2 strings represent binary data and to prefix all byte-string literals for binary
data with ``b`` like ``b'\x00ABCD'``.

After stage 2 conversion, all string literals for textual data without ``b``
prefixes will use Python 3's ``str`` type (or the backported ``str`` object
from ``future`` on Python 2).


.. _forwards-conversion-stage2:

Stage 2: Py3 code with ``future`` wrappers for Py2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal for this step is to get the tests passing first on Py3 and then on Py2
again with the help of the ``future`` package.

Run with::

    futurize —-stage2 myfolder/*.py

This adds three further imports::

    from __future__ import unicode_literals
    from future import standard_library
    from future.builtins import *

to each module and makes other changes needed to support Python 3, such as
renaming standard-library imports to their Py3 names.

All strings are then unicode (on Py2 as on Py3) unless explicitly marked with a ``b''`` prefix.

Ideally the output of this stage should not be a ``SyntaxError`` on either
Python 3 or Python 2.

After this, you can run your tests on Python 3 and make further code changes
until they pass on Python 3.

The next step would be manually adding wrappers from ``future`` to re-enable
Python 2 compatibility. See :ref:`what-else` for more info.


.. _backwards-conversion:

Backwards: 3 to both
--------------------

Running ``futurize --from3`` turns this Python 3 code::
    
    import configparser
    
    class Blah:
        pass
    print('Hello', end=None)

into this code which runs on both Py2 and Py3::
    
    from __future__ import print_function
    from future import standard_library
    
    import configparser

    class Blah(object):
        pass
    print('Hello', end=None)

Notice that in both this case and when converting from Py2 above,
``futurize`` creates a new-style class on both Python versions and
imports the renamed stdlib module under its Py3 name.

``futurize --from3`` also handles the following Python 3 features:

- keyword-only arguments
- metaclasses (using :func:`~future.utils.with_metaclass`)
- extended tuple unpacking (PEP 3132)

To handle function annotations (PEP 3107), see
:ref:`func_annotations`.


How well does ``futurize`` work?
--------------------------------

It is still incomplete and makes mistakes, like 2to3, on which it is
based.

Nevertheless, ``futurize`` is useful to automate much of the work
of porting, particularly the boring repetitive text substitutions. It
also helps to flag which parts of the code require attention.

Please report bugs on `GitHub
<https://github.com/PythonCharmers/python-future/>`_.

Contributions to ``futurize`` are particularly welcome! Please see :ref:`contributing`.


.. _futurize-limitations

Known limitations of ``futurize``
---------------------------------

``futurize`` doesn't currently make any of these changes automatically::

1. A source encoding declaration line like::
    
       # -*- coding:utf-8 -*-
  
   is not kept at the top of a file. It must be moved manually back to line 1 to take effect.

2. Strings containing ``\U`` produce a ``SyntaxError`` on Python 3. An example is::

       s = 'C:\Users'.

   Python 2 expands this to ``s = 'C:\\Users'``, but Python 3 requires a raw
   prefix (``r'...'``). This also applies to multi-line strings (including
   multi-line docstrings).


