import unittest

from future.types.exceptions.base import message_checking_exception


class TestMessageChecking(unittest.TestCase):
    def test_positive_match(self):
        try:
            raise Exception("You can match me")
        except message_checking_exception("match") as e:
            pass
        except Exception:
            raise AssertionError("Did not catch exception")

    def test_no_match(self):
        try:
            raise Exception("You can match me")
        except message_checking_exception("nomatch") as e:
            raise AssertionError("Erroneously caught exception")
        except Exception:
            pass

    def test_nomatch_followed_by_match_matches(self):
        try:
            raise Exception("You can match me")
        except message_checking_exception("nomatch") as e:
            raise AssertionError("Erroneously caught exception")
        except message_checking_exception("match") as e:
            pass
        except Exception:
            raise AssertionError("Did not catch exception")
