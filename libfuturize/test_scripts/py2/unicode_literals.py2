'''
Tests to ensure that the u'' and b'' prefixes on unicode and byte strings
are not removed.  Removing the prefixes on Py3.3+ is unnecessary and
loses some information -- namely, that the strings have explicitly been
marked as unicode, rather than just our guess (perhaps incorrect) that
they should be unicode or bytes.
'''

s = u'mystring'
b = b'mybytes'
icons = [u"◐", u"◓", u"◑", u"◒"]
