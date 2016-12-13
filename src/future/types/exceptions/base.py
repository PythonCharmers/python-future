"""
Libraries are not as fine-grained with exception classes as one would like. By
using this hack, you can make create your own exceptions which behave as if
they are superclasses of the ones raised by the standard library.

Tread with caution.

Defines the base `instance_checking_exception` creator.
"""

import re
import sys


def instance_checking_exception(base_exception=Exception):
    def wrapped(instance_checker):
        """
        Create an exception class which inspects the exception being raised.

        This is most easily used as a decorator:

        >>> @instance_checking_exception()
        ... def Foo(inst):
        ...     return "Foo" in inst.message
        >>> try:
        ...     raise Exception("Something Fooish")
        ... except Foo as e:
        ...     print "True"
        ... except Exception:
        ...     print "False"
        True

        This is quite a powerful tool, mind you.

        Arguments:
            instance_checker (callable): A function which checks if the given
                instance should be treated as an instance of a (subclass) of this
                exception.

        Returns:
            Exception: (Actually: a new subclass of it), which calls the argument
                `instance_checker` when it is checked against during exception
                handling logic.
        """
        class TemporaryClass(base_exception):
            def __init__(self, *args, **kwargs):
                if len(args) == 1 and isinstance(args[0], TemporaryClass):
                    unwrap_me = args[0]
                    for attr in dir(unwrap_me):
                        if not attr.startswith('__'):
                            setattr(self, attr, getattr(unwrap_me, attr))
                else:
                    super(TemporaryClass, self).__init__(*args, **kwargs)

            class __metaclass__(type):
                def __instancecheck__(cls, inst):
                    return instance_checker(inst)

                def __subclasscheck__(cls, classinfo):
                    value = sys.exc_info()[1]
                    return isinstance(value, cls)

        TemporaryClass.__name__ = instance_checker.__name__
        TemporaryClass.__doc__ = instance_checker.__doc__
        return TemporaryClass
    return wrapped
