
limitations of the ``future`` module
=========================================

The following attributes on functions in Python 3 are not provided in Python
2.7:

__func__: see six.get_method_function()
__self__: see six.get_method_self()
__self__.__class__

Builtins that call methods: __next__, __str__ on Py3 versus next and
__unicode__ on Py2. Requires mixin classes or decorators or something fancy.

Limitations / TODO
------------------
Some new Python 3.3 features that cause SyntaxErrors on earlier versions
are not currently handled by the ``futurize`` script. This includes:

- ``yield ... from`` syntax for generators in Py3.3

- ``raise ... from`` syntax for exceptions. (This is simple to fix
  manually by creating a temporary variable.)

Also:

- Usage of ``file('myfile', 'w')`` as a synonym for ``open`` doesn't seem
  to be converted currently.

- ``isinstance(var, basestr)`` should sometimes be converted to
  ``isinstance(var, str) or isinstance(var, bytes)``. Currently it is
  always converted to ``isinstance(var, str)``.

- Caveats with bytes indexing!!!::

      b'\x00'[0] != 0
      b'\x01'[0] != 1
  
  This is difficult to handle portable between Py2 and Py3, because
  Python 2's bytes object is merely an alias for Python 2's str, which is
  very different from Python 3's bytes object.


Notes
-----
- Ensure you are using new-style classes on Py2. Py3 doesn't require
  inheritance from ``object`` for this, but Py2 does. ``futurize
  --from3`` adds this back in automatically, but ensure you do this too
  when writing your classes, otherwise weird breakage when e.g. calling
  ``super()`` may occur.



