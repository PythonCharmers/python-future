"""
This module redefines str on Python 2.x to be the unicode type.

It is designed to be used together with the unicode_literals import as
follows:

    from __future__ import unicode_literals
    from future import str_is_unicode

On Python 3.x and normally on Python 2.x, this expression:

    str('blah') is 'blah'

return True.

However, on Python 2.x, with this import:

    from __future__ import unicode_literals

the same expression

    str('blah') is 'blah'

returns False.

This module is designed to be imported together with unicode_literals on
Python 2 to bring the meaning of str() back into alignment with
unprefixed
string literals.

Note that str() will then call the __unicode__ method on objects in
Python 2, whereas print() will call __str__.
"""

from __future__ import unicode_literals

import inspect

from . import six


if not six.PY3:
    caller = inspect.currentframe().f_back
    caller.f_globals['str'] = unicode

