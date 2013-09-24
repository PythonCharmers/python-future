Explicit imports
----------------
If you prefer explicit imports, the explicit equivalent of the ``from
future.builtins import *`` line is::

    from future.builtins import (zip, map, filter,
                                 ascii, oct, hex, chr, input,
                                 bytes, range, super, round,
                                 apply, cmp, coerce, execfile, file, long,
                                 raw_input, reduce, reload, unicode, xrange,
                                 str, StandardError)

To understand what each of these does, see the docs for these modules:

- future.builtins
- future.builtins.iterators
- future.builtins.misc
- future.builtins.backports
- future.builtins.disabled
- future.builtins.str_is_unicode

The internal API is currently as follows::
    
    from future.builtins.iterators import zip, map, filter
    from future.builtins.misc import ascii, oct, hex, chr, input
    from future.builtins.backports import bytes, range, super, round
    from future.builtins.disabled import (apply, cmp, coerce,
            execfile, file, long, raw_input, reduce, reload, unicode,
            xrange, StandardError)
    from future.builtins.str_is_unicode import str

But please note that this internal API is still evolving rapidly.

