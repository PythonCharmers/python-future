"""
Tests whether the existing __future__ statement is preserved and not
duplicated or moved below some executable statement.
"""

from __future__ import absolute_import
from __future__ import print_function

import socketserver
print('blah')
