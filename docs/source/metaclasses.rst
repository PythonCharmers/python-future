Metaclasses
-----------

Python 3 and Python 2 syntax for metaclasses are incompatible. The new syntax 
should ideally be available in Python 2 as a `__future__`` import like ``from 
__future__ import new_metaclass_syntax``. Since this is not available,
``future`` provides a function (from ``jinja2/_compat.py``) called
``with_metaclass`` that can assist with specifying metaclasses portably across
Py3 and Py2. Use it like this::
        
    from future.utils import with_metaclass

    class BaseForm(object):
        pass
    
    class FormType(type):
        pass
    
    class Form(with_metaclass(FormType, BaseForm)):
        pass


