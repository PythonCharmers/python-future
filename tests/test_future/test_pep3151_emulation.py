import errno
import os
import re
import unittest

from future.types.exceptions import pep3151
from future.builtins import FileNotFoundError, NotADirectoryError, PermissionError

MISSING_FILE = "/I/sure/hope/this/does/not.exist"

class TestPEP3151LikeSuperClassing(unittest.TestCase):
    def test_catching_enoent_from_open(self):
        try:
            open(MISSING_FILE)
        except FileNotFoundError as e:
            assert e.errno == errno.ENOENT
            assert e.filename == MISSING_FILE
        except Exception as e:
            raise AssertionError("Could not create proper exception:" + str(e))

    def test_catching_enoent_from_remove(self):
        try:
            os.remove(MISSING_FILE)
        except FileNotFoundError as e:
            assert e.filename == MISSING_FILE
        except Exception as e:
            raise AssertionError("Could not create proper exception:" + str(e))

    def test_not_catching_non_enoent(self):
        try:
            os.listdir(__file__)
        except FileNotFoundError:
            raise AssertionError(
                "Opening `/` raised FileNotFoundError, should be ENOTDIR"
            )
            pass
        except OSError as e:
            assert e.errno == errno.ENOTDIR

    def test_catching_enotdir_from_listdir(self):
        try:
            os.listdir(__file__)
        except NotADirectoryError:
            pass
        except Exception as e:
            raise AssertionError("Could not create proper exception:" + str(e))

    def test_all_errnos_defined(self):
        # An extra sanity check against typos in the errno definitions.
        path = pep3151.__file__
        if path.endswith("pyc"):
            path = path[:-1]

        with open(path, 'r') as fp:
            contents = fp.read()

        for match in re.finditer(r"\berrno\.([A-Z]+)\b", contents):
            assert hasattr(errno, match.group(1)), match.group(1)
