"""
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
            # def __new__(cls, *args):
            #     print('TemporaryClass.__new__: args are: {0}'.format(args))
            #     if len(args) == 1 and isinstance(args[0], TemporaryClass):
            #         unwrap_me = args[0]
            #         err = super(TemporaryClass, cls).__new__(cls)
            #         for attr in dir(unwrap_me):
            #             if not attr.startswith('__'):
            #                 setattr(err, attr, getattr(unwrap_me, attr))
            #     else:
            #         return super(base_exception, cls).__new__(cls, *args) 
        
            def __init__(self, *args, **kwargs):
                # print('TemporaryClass.__init__: args are: {0}'.format(args))
                if len(args) == 1 and isinstance(args[0], TemporaryClass):
                    unwrap_me = args[0]
                    for attr in dir(unwrap_me):
                        if not attr.startswith('__'):
                            setattr(self, attr, getattr(unwrap_me, attr))
                else:
                    super(TemporaryClass, self).__init__(*args, **kwargs)

            class __metaclass__(type):
                def __instancecheck__(cls, inst):
                    # print('FileNotFoundError.__isinstance__: type(inst) = {0}\ninst = {1}'.format(type(inst), inst))
                    return instance_checker(inst)

                def __subclasscheck__(cls, classinfo):
                    # print('In __subclasscheck__:\n\tcls = {0}\n\tclassinfo = {1}'.format(cls, classinfo))
                    # return instance_checker(classinfo)
                    # This hook is called during the exception handling.
                    # Unfortunately, we would rather have exception handling call
                    # __instancecheck__, so we have to do that ourselves. But,
                    # that's not how it currently is.  If you feel like proposing a
                    # patch for Python, check the function
                    # `PyErr_GivenExceptionMatches` in `Python/error.c`.
                    value = sys.exc_info()[1]
                    # if value is None:
                    #     print('Exception value is None!!')

                    # Double-check that the exception given actually somewhat
                    # matches the classinfo we received. If not, people may be using
                    # `issubclass` directly, which is of course prone to errors,
                    # or they are raising the exception with `raise ...`
                    # if value.__class__ != classinfo:
                    #     print('Mismatch!\nvalue: {0}\nvalue.__class__: {1}\nclassinfo: {2}'.format(
                    #         value, value.__class__, classinfo)
                    #     )
                    return isinstance(value, cls)

        TemporaryClass.__name__ = instance_checker.__name__
        TemporaryClass.__doc__ = instance_checker.__doc__
        return TemporaryClass
    return wrapped


def message_checking_exception(regex, classname=None):
    """
    Create exception class which matches message against regular expression.

    >>> Foo = message_checking_exception("Fooish", "Foo")
    >>> Foo.__class__.__name__
    'Foo'
    >>> try:
    ...     raise Exception("Something Fooish")
    ... except Foo:
    ...     print "True"
    ... except Exception:
    ...     print "False"
    True

    Arguments:
        regex (string|RE): A regular expression which will be matched against
            the `.message` attribute of the exception raised. Note that it uses
            `re.search`, so if you want to match the beginning you have to
            explicitly anchor the string (using `\A` or `^`).

    Returns:
        Exception: (Actually: a new subclass of it), which checks the message
            of the exception against the supplied regex.
    """
    @instance_checking_exception
    def check_message(inst):
        return re.search(regex, inst.message)
    if classname is not None:
        check_message.__class__.__name__ = classname
    return check_message
