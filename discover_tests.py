"""
Simple auto test discovery.

From http://stackoverflow.com/a/17004409
"""
import os
import sys
import unittest

def additional_tests():
    setup_file = sys.modules['__main__'].__file__
    setup_dir = os.path.abspath(os.path.dirname(setup_file))
    return unittest.defaultTestLoader.discover(setup_dir)
