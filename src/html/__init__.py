from __future__ import absolute_import
import sys
__future_module__ = True

if sys.version_info[0] == 3:
    raise ImportError('Cannot import module from python-future source folder')

else:
    # cgi.escape isn't good enough for the single Py3.3 html test to pass.
    # Define it inline here instead. From the Py3.3 stdlib
    """
    General functions for HTML manipulation.
    """


    _escape_map = {ord('&'): '&amp;', ord('<'): '&lt;', ord('>'): '&gt;'}
    _escape_map_u = {k: unicode(v) for k, v in _escape_map.items()}
    _escape_map_full = {ord('&'): '&amp;', ord('<'): '&lt;', ord('>'): '&gt;',
                        ord('"'): '&quot;', ord('\''): '&#x27;'}
    _escape_map_full_u = {k: unicode(v) for k, v in _escape_map_full.items()}

    def escape(s, quote=True):
        """
        Replace special characters "&", "<" and ">" to HTML-safe sequences.
        If the optional flag quote is true (the default), the quotation mark
        characters, both double quote (") and single quote (') characters are
        also translated.
        """
        if quote:
            return s.translate(_escape_map_full
                               if isinstance(s, str)
                               else _escape_map_full_u)
        return s.translate(_escape_map
                           if isinstance(s, str)
                           else _escape_map_u)
