dictionary iterator methods
-----------------------------

Python 3 dictionaries have ``.keys()``, ``.values()``, and ``.items()``
methods which return memory-efficient set-like objects, not lists. (See
`PEP 3106 <http://www.python.org/dev/peps/pep-3106/>`_.)

If your dictionaries are small enough that the memory overhead of extra
list creation is not significant, stick with standard Python 3 code in
your Py3/2 compatible codebase::

    for item in d:
        # code here

    for item in d.items():
        # code here
    
    for value in d.values():
        # code here


If your dictionaries are large, or if you want to use the Python 3
set-like behaviour on both Py3 and Python 2.7, then use the ``viewkeys``
etc. functions from :mod:`future.utils`::

    from future.utils import viewkeys, viewvalues, viewitems

    for (key, value) in viewitems(hugedictionary):
        # some code here
    
    # Set intersection:
    d = {i**2: i for i in range(1000)}
    both = viewkeys(d) & set(range(0, 1000, 7))
     
    # Set union:
    both = viewvalues(d1) | viewvalues(d2)

