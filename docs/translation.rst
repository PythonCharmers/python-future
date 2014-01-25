.. _translation:

``future.translation`` package [Experimental]
=============================================

``future`` now provides an experimental ``translation`` package to help
with importing and using old Python 2 modules in a Python 3 environment.

This is implemented using PEP 414 import hooks together with fixers from
``lib2to3`` and ``libfuturize`` (included with ``python-future``) that
attempt to automatically translate Python 2 code to Python 3 syntax and
semantics upon import.

*Note* This feature is still in alpha and needs further development to support a
full range of real-world Python 2 modules. Also be aware that the API for
this package might change considerably in later versions.

Here is how to use it::

    $ pip3 install plotrique==0.2.5-7 --no-compile   # to ignore SyntaxErrors
    $ python3
    
Then pass in a whitelist of module name prefixes to the
``future.autotranslate()`` function. Example::
    
    >>> from future import autotranslate
    >>> autotranslate('plotrique')
    >>> import plotrique

Here is a more explicit example::

    >>> from future.translation import install_hooks
    >>> install_hooks()
    >>> import mypy2module

This will translate, import and run Python 2 code such as the following::

    ### File: mypy2module.py

    # Print statements are translated transparently to functions:
    print 'Hello from a print statement'
     
    # xrange() is translated to Py3's range():
    total = 0
    for i in xrange(10):
        total += i
    print 'Total is: %d' % total
    
    # Dictionary methods like .keys() and .items() are supported and
    # return lists as on Python 2:
    d = {'a': 1, 'b': 2}
    assert d.keys() == ['a', 'b']
    assert isinstance(d.items(), list)
    
    # Functions like range, reduce, map, filter also return lists:
    assert isinstance(range(10), list)

    # The exec statement is supported:
    exec 'total += 1'
    print 'Total is now: %d' % total

    # Long integers are supported:
    k = 1234983424324L
    print 'k + 1 = %d' % k

    # Most renamed standard library modules are supported:
    import ConfigParser
    import HTMLParser
    import urllib


The attributes of the module are then accessible normally from Python 3.
For example::
    
    # This Python 3 code works
    >>> type(mypy2module.d)
    builtins.dict

This is a standard Python 3 data type, so, when called from Python 3 code,
``keys()`` returns a view, not a list::

    >>> type(mypy2module.d.keys())
    builtins.dict_keys


.. _translation-limitations

Known limitations of ``future.translation``
-------------------------------------------

The source translation feature offered by the ``future.translation``
package has the same limitations as the ``futurize`` script (see
:ref:`_futurize-limitations`_). Help developing and testing this further
would be particularly welcome.

Please report any bugs you find on the ``python-future`` `bug tracker
<https://github.com/PythonCharmers/python-future/>`_.