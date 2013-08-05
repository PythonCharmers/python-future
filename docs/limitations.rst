
limitations of the ``future`` module
=========================================

The following attributes on functions in Python 3 are not provided in Python
2.7:

__func__: see six.get_method_function()
__self__: see six.get_method_self()
__self__.__class__

Builtins that call methods: __next__, __str__ on Py3 versus next and
__unicode__ on Py2. Requires mixin classes or decorators or something fancy.
