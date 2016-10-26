# The following three can be changed
ALWAYS_AVOID = []
ALWAYS_AVOID_REPL = []
AUTOLOAD_ALL = True

# ------------------------------------------------------------------------
# ***************** Known bug ********************************************
# ------------------------------------------------------------------------
# If using AUTOLOAD_ALL=True, AND 'unicode' is not in ALWAYS_AVOID,
# pydoc2 (pydoc on python2) will fail for this module.
# To use pydoc on py23compat with AUTOLOAD_ALL=True, do one of the
# following:
#
#   - Use pydoc3 in a python3 virtualenv
#   - In a REPL, import py23compat and then do help(py23compat)
#   - Call pydoc setting (shell) environment var PY23COMPAT_NO_AUTOLOAD)
#   - Alias pydoc to 'PY23COMPAT_NO_AUTOLOAD=yes pydoc'
#
# Note that PY23COMPAT_NO_AUTOLOAD disables effect of AUTOLOAD_ALL in
# ALL conditions- not just for pydoc - there is no way to effect special
# behavior when being imported by pydoc
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Shouldn't have to change anything below this
# ------------------------------------------------------------------------

import sys
v_info = sys.version_info
(PY2, PY3) = (v_info.major == 2, v_info.major == 3)
PY_MINOR = v_info.minor
PYPY = (PY2 and sys.subversion[0].lower() == 'pypy')
del v_info
import warnings
if PY2 and PY_MINOR < 6:
    warnings.warn('p23compat fixups will not work in Python2 < 2.6')

MARKER = '__inject_compat_done__'
globals()[MARKER] = True     # Never need to inject into THIS module
IN_REPL = hasattr(sys, 'ps1')
future_imports = ['absolute_import', 'division',
                  'print_function', 'unicode_literals']
builtins_imports = [
    'ascii', 'bytes', 'chr', 'dict', 'filter', 'hex', 'input',
    'int', 'map', 'next', 'oct', 'open', 'pow', 'range', 'round',
    'str', 'super', 'zip',
]
obsolete_imports = [
    'apply', 'cmp', 'coerce', 'execfile', 'file', 'long', 'raw_input',
    'reduce', 'reload', 'unicode', 'xrange', 'StandardError',
]


def is_str(x):
    '''
    Returns-->boolean
    On Python 2 matches 'unicode' and 'str.  On Python 3, matches ONLY 'str'

    '''
    if PY2:
        return isinstance(x, unicode)
    else:
        return isinstance(x, str)


def is_int(x):
    '''
    Returns-->boolean
    On Python 2 matches 'long' and 'int.  On Python 3, matches ONLY 'int'
    '''
    if PY2:
        return isinstance(x, (int, long))
    else:
        return isinstance(x, int)


def inject_compat(avoid=None):
    '''
    avoid-->LIST of strings: imports to avoid
    This is in ADDITION to ALWAYS_AVOID above (non-REPL use) and in
    ADDITION to ALWAYS_AVOID_REPL above (for REPL use).
    '''
    if PY2 and PY_MINOR < 6:
        return
    if avoid is None:
        avoid = []
    avoid_keys = dict.fromkeys(avoid)
    avoid_keys.update(dict.fromkeys(ALWAYS_AVOID))
    avoid_keys_repl = dict.fromkeys(avoid)
    avoid_keys_repl.update(dict.fromkeys(ALWAYS_AVOID_REPL))

    callerframe = sys._getframe(1)
    # When in REPL, inject compatibility into top-most frame (also)
    if IN_REPL:
        topframe = callerframe
        while topframe.f_back is not None:
            topframe = topframe.f_back
        framelist = [callerframe, topframe]
    else:
        topframe = None
        framelist = [callerframe]
    if AUTOLOAD_ALL and AUTOLOAD:
        if callerframe.f_back is not None:
            framelist += [callerframe.f_back]

    d = get_import_dict()

    for frame in framelist:
        if MARKER in frame.f_globals:
            continue

        if topframe and IN_REPL:
            avoid_dict = avoid_keys_repl
        else:
            avoid_dict = avoid_keys

        for (k, v) in d.items():
            if k not in avoid_dict:
                frame.f_globals[k] = v

        if frame is topframe and IN_REPL:
            b = frame.f_globals['__builtins__']
            if isinstance(b, dict):
                b['is_int'] = is_int
                b['is_str'] = is_str
            else:
                setattr(b, 'is_int', is_int)
                setattr(b, 'is_str', is_str)

        frame.f_globals[MARKER] = True


def import_to_dict(d, mod_name, name_list):
    '''
    d-->dict
    mod_name-->str
    name_list-->LIST of str
    Returns-->Nothing: modifies d

    Only intended to be called from get_import_dict
    '''
    import importlib
    try:
        mod = importlib.import_module(mod_name)
    except:
        return
    for name in name_list:
        if hasattr(mod, name):
            d[name] = getattr(mod, name)


def get_import_dict():
    '''
    Returns-->dict

    Only intended to be called by inject_compat
    '''
    import future      # noqa: F401
    import builtins    # noqa: F401

    ret = {}
    import_to_dict(ret, '__future__', future_imports)
    import_to_dict(ret, 'future.builtins', builtins_imports)
    import_to_dict(ret, 'future.builtins.disabled', obsolete_imports)
    return ret


# Inject compatibility by JUST importing this module
# but ONLY when running in interactive mode
AUTOLOAD = False
if IN_REPL:
    inject_compat()

# Allow pydoc when using AUTOLOAD_ALL by setting env var
import os

if AUTOLOAD_ALL and 'PY23COMPAT_NO_AUTOLOAD' not in os.environ:
    AUTOLOAD = True
    inject_compat()

__doc__ = '''
Dependencies:
------------
    Uses and requires installation of the excellent 'future' package.
    Install with pip install future

    This module has no other external dependencies. You can place it
    anywhere on your PYTHONPATH

    Does not work with Python2 < 2.6 - importing this module or calling
    inject_compat() should have no effect in such cases

Four capabilities, three variables to set and one method:
--------------------------------------------------------
    Capability                              Variable / Method
    ----------                              --------
    Customize features for source files     ALWAYS_AVOID variable
    Customize features for REPL             ALWAYS_AVOID_REPL variable
    Select features by just importing       AUTOLOAD_ALL variable
    Select features on per-file basis       inject_compat method

    AUTOLOAD_ALL versus calling inject_compat:
        If you want to choose different features for different source
        files, you NEED TO:
            Add following TWO lines to the top of each source file
                from py23compat import inject_compat
                inject_compat()
            You can avoid SOME features across ALL source files by
            adding those features to ALWAYS_AVOID, and add ADDITIONAL
            features to avoid on a per-file basis by adding avoid=[...]
            to the inject_compat() call in each source file

            In this model, you NEED to add TWO lines to each source file,
            though you may not need the avoid=[..] in the call to
            inject_compat in all source files.

        If all your source files are in the SAME STAGE of Python-2-3
        compatibility / migration, you can:
            Disable some features across ALL source files using
            ALWAYS_AVOID
            Set AUTOLOAD_ALL = True
            Load remaining features in each source file by JUST importing
            py23compat using a line like:
                import py23compat     # noqa: F401

            '# noqa: F401' asks PEP8 not to complain about an unused import

            In this model, you CANNOT customize features on a per-file
            basis.

    The features avoided in the REPL are separate (ALWAYS_AVOID_REPL).
    Features are ALWAYS injected into the REPL by JUST importing py23compat.

is_int and is_str methods:
-------------------------
    Some modules (such as simplejson, but I am sure there are more), can
    RETURN objects of type 'unicode' or 'long' in Python2. If you have
    disabled 'unicode' and 'long' in Python2 (e.g. by having an empty
    ALWAYS_AVOID list), then you have no way to check if the returned
    valus is an instance of 'unicode' or 'long' respectively. In addition,
    in such cases, the returned variable will NOT be an instance of
    str | int respectively (although it's BEHAVIOR will be similar to those
    respective types).

    In such cases, you can use the is_str and is_int methods by importing
    them from this module. On Python2 is_int will match int and long and
    is_str will match str and unicode, while on Python3 is_int will match
    only int and is_str will match only str.

    You only need these methods if you would have otherwise used isinstance
    for this purpose.

Python version variables:
------------------------
    PY2-->boolean: Whether running in python2 (any minor version)
    PY3-->boolean: Whether running in python3 (any minor version)
    PYPY-->boolean: Whether running in pypy (any minor version)
    PY_MINOR-->int: Python minor version

Variables, imports and what is injected:
---------------------------------------
    REPL    Variable            import          Effect
    -----------------------------------------------------------------------
    YES     ALWAYS_AVOID_REPL   plain import    Except ALWAYS_AVOID_REPL
                                                is_int and is_str automatic

    YES     ALWAYS_AVOID_REPL   import +        Except ALWAYS_AVOID_REPL
            avoid param         inject_compat   avoid param has no effect
                                                is_int, is_str need import

    Source  ALWAYS_AVOID        plain import    Except ALWAYS_AVOID
                                                is_int, is_str need import

    Source  ALWAYS_AVOID        import +        Except ALWAYS_AVOID AND
            avoid param         inject_compat   except avoid param
                                                is_int, is_str need import
    -----------------------------------------------------------------------

    inject_compat ONLY injects compatibility names into:
        Caller's stack frame
        Top-most stack frame ONLY if running in REPL

    Importing this module ONLY injects compatibility names into:
        Top-most stack frame ONLY if running in REPL
        Into caller's (importer's) stack frame if AUTOLOAD_ALL is set

    When using the REPL, if ANY module IMPORTS py23compat, the
    compatibility names will be injected into the TOP-MOST stack
    frame (repeat: ONLY when using the REPL)

    Note the difference between the CALLER (importer) stack frame and
    the TOP-MOST stack frame.

Usage for NEW python packages starting from scratch:
---------------------------------------------------
    A. Make a COPY of this module (file) for EACH package - it has
       variables at the top that you CAN (and SHOULD) change to reflect
       the stage the package is in  (in terms of Python2-3 compatibility)

    B. For a NEW package started from scratch, I recommend:
        1. Keep ALWAYS_AVOID and ALWAYS_AVOID_REPL EMPTY
        2. Set AUTOLOAD_ALL = True
            Allows injecting compatibility code by JUST importing py23compat
            Still obeys ALWAYS_AVOID and ALWAYS_AVOID_REPL
            if you need them
        3. Write your package using (only) Python3 idioms and constructs.
          It should run unchanged in Python2 (need to pip install future)

Usage for making existing Python2 packages compatible with Python2-3:
--------------------------------------------------------------------

    A. Make a COPY of this module (file) for EACH package - it has
       variables at the top that you CAN (and SHOULD) change to reflect
       the stage the package is in  (in terms of Python2-3 compatibility)

    B. Make a list of all the changed features and obsoleted features
       being used by your package.
            See future_imports for NEW behavior in Python3
            See builtins_imports for CHANGED behavior
            See obsolete_imports for OBSOLETED classes, methods

    E. Use one of the following strategies. Note there are MANY possible
       strategies, and the python-future website has a much more robust
       and complete discussion of migration strategies.

        Feature-by-feature
            1. Start by adding ALL the features your package is using that has
               been changed or obsoleted in Python3 to ALWAYS_AVOID.

            2. If you regularly explore your package interactively using a REPL,
                add JUST the changed features (not the obsoleted features) to
                ALWAYS_AVOID_REPL also.

            3. Go through your package feature-by-feature and once a
                feature has been upgraded across your package, remove it
                from ALWAYS_AVOID and ALWAYS_AVOID_REPL.

            4. During this time, you can keep AUTOLOAD_ALL = True and
               JUST import py23compat at the top of each source file

            5. Once you have emptied ALWAYS_AVOID and ALWAYS_AVOID_REPL,
               your package should run unchanged in Python 2 and 3

        File-by-file
            1. Add two lines at the top of each source file:
                   from py23compat import inject_compat
                   inject_compat(avoid=xyz)
               where xyz is a set of features to disable for that file

            2. In each file, upgrade each disabled feature and then
               remove it from the avoid list

            3. Once the avoid list is empty, you can change the two lines
               at the top to be just:
                   import py23compat

            4. Once all files have been upgraded and have an empty avoid list,
               your package should run unchanged in Python 2 and 3

Known bug: interaction with pydoc on Python2:
--------------------------------------------
If using AUTOLOAD_ALL=True, AND 'unicode' is not in ALWAYS_AVOID,
pydoc2 (pydoc on python2) will fail for this module.
To use pydoc on py23compat with AUTOLOAD_ALL=True, do one of the
following:

  - Use pydoc3 in a python3 virtualenv
  - In a REPL, import py23compat and then do help(py23compat)
  - Call pydoc setting (shell) environment var PY23COMPAT_NO_AUTOLOAD)
  - Alias pydoc to 'PY23COMPAT_NO_AUTOLOAD=yes pydoc'

Note that PY23COMPAT_NO_AUTOLOAD disables effect of AUTOLOAD_ALL in
ALL conditions- not just for pydoc - there is no way to effect special
behavior when being imported by pydoc


More information on python-future and Python2-3 compatibility:
-------------------------------------------------------------
    See the python-future site for more information on writing python
    programs that can run in Python 2.x or 3.x, Python 2-->3 migration
    and the python-future package.

    Python-future Quick Start Guide: http://python-future.org/quickstart.html

    Idioms for writing Python 2-3 compatible code:
        http://python-future.org/compatible_idioms.html

    Importing explicitly:
    http://python-future.org/imports.html#explicit-imports

The contents of future_imports, builtins_imports and obsolete_imports
are below. These are the imports that can be customized with the 'avoid'
keyword to inject_compat:


'''
__doc__ += '''
future_imports = %s

builtins_imports = %s

obsolete_imports = %s
''' % (
    str(future_imports), str(builtins_imports), str(obsolete_imports)
)
