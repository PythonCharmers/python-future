.. _automatic-conversion:

Automatic conversion with ``futurize``
======================================

The ``future`` source tree includes an experimental script called ``futurize``
to aid in making either Python 2 code or Python 3 code compatible with both
platforms using the ``future`` module. It is based on 2to3 and uses fixers from
``lib2to3``, ``lib3to2``, and ``python-modernize``.

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

Notice that in both cases ``futurize`` forces a new-style class and
imports the renamed stdlib module under its Py3 name.

It also handles the following Python 3 features:

- keyword-only arguments
- metaclasses (using ``future.utils.with_metaclass``)


How well does ``futurize`` work?
--------------------------------
It is incomplete and makes mistakes, like 2to3, on which it is based.

``futurize`` is still useful to automate much of the boring repetitive
text substitutions needed for the porting effort.

Please report bugs on `GitHub <http://github.com/edschofield/python-future/>`_.


