from __future__ import absolute_import, unicode_literals
from future.utils import PY3

if PY3:
    from html import *
else:
    __future_module__ = True

    # cgi.escape isn't good enough for the single Py3.3 html test to pass.
    # Define it inline here instead. From the Py3.3 stdlib
    """
    General functions for HTML manipulation.
    """


    _escape_map = {ord('&'): '&amp;', ord('<'): '&lt;', ord('>'): '&gt;'}
    _escape_map_full = {ord('&'): '&amp;', ord('<'): '&lt;', ord('>'): '&gt;',
                        ord('"'): '&quot;', ord('\''): '&#x27;'}

    # NB: this is a candidate for a bytes/string polymorphic interface

    def escape(s, quote=True):
        """
        Replace special characters "&", "<" and ">" to HTML-safe sequences.
        If the optional flag quote is true (the default), the quotation mark
        characters, both double quote (") and single quote (') characters are also
        translated.
        """
        if quote:
            return s.translate(_escape_map_full)
        return s.translate(_escape_map)
