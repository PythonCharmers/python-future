"""
Exception matching patchwork.

Libraries are not as fine-grained with exception classes as one would like. By
using exhacktion, you can make create your own exceptions which behave as if
they are superclasses of the ones raised by the library.

Tread with caution.
"""

from .pep3151 import *
