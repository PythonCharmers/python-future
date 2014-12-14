.. _backwards-conversion:

``pasteurize``: Py3 to Py2/3
----------------------------

Running ``pasteurize -w mypy3module.py`` turns this Python 3 code::
    
    import configparser
    
    class Blah:
        pass
    print('Hello', end=None)

into this code which runs on both Py2 and Py3::
    
    from __future__ import print_function
    from future import standard_library
    standard_library.install_hooks()
    
    import configparser

    class Blah(object):
        pass
    print('Hello', end=None)

Notice that both ``futurize`` and ``pasteurize`` create explicit new-style
classes that inherit from ``object`` on both Python versions, and both 
refer to stdlib modules (as well as builtins) under their Py3 names.

``pasteurize`` also handles the following Python 3 features:

- keyword-only arguments
- metaclasses (using :func:`~future.utils.with_metaclass`)
- extended tuple unpacking (PEP 3132)

To handle function annotations (PEP 3107), see :ref:`func_annotations`.



