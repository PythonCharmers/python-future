How well do ``futurize`` and ``pasteurize`` work?
-------------------------------------------------

They are still incomplete and make some mistakes, like 2to3, on which they are
based.

Nevertheless, ``futurize`` and ``pasteurize`` are useful to automate much of the
work of porting, particularly the boring repetitive text substitutions. They also
help to flag which parts of the code require attention.

Please report bugs on `GitHub
<https://github.com/PythonCharmers/python-future/>`_.

Contributions to the ``lib2to3``-based fixers for ``futurize`` and
``pasteurize`` are particularly welcome! Please see :ref:`contributing`.


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


