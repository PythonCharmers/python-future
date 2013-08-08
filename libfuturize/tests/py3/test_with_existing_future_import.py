"""
An example Python 3 script with an existing __future__ import.
We don't want libfuturize to clobber or duplicate this ...
"""

from __future__ import absolute_import

import urllib.parse
import urllib.request
import urllib.error
import http.client
import email.message
import io
import unittest
from test import support
import os
import sys
import tempfile

from base64 import b64encode
import collections

