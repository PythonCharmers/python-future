"""
For the ``future`` package.

Fixer for itertools methods that no longer deviate from builtins.

This applies to imap, izip, and ifilter

Adds this import line:

    from builtins import filter, map, zip

at the top.
"""

from lib2to3 import fixer_base

from libfuturize.fixer_util import touch_import_top

filter_expression = "name='ifilter'"
map_expression = "name='imap'"
zip_expression = "name='izip'"

class FixFilter(fixer_base.BaseFix):

    PATTERN = """
              power<
                 ({0}) trailer< '(' args=[any] ')' >
              rest=any* >
              """.format(filter_expression)

    def transform(self, node, results):
        touch_import_top(u'builtins', 'filter', node)

class FixMap(fixer_base.BaseFix):

    PATTERN = """
              power<
                 ({0}) trailer< '(' args=[any] ')' >
              rest=any* >
              """.format(map_expression)

    def transform(self, node, results):
        touch_import_top(u'builtins', 'map', node)

class FixZip(fixer_base.BaseFix):

    PATTERN = """
              power<
                 ({0}) trailer< '(' args=[any] ')' >
              rest=any* >
              """.format(zip_expression)

    def transform(self, node, results):
        touch_import_top(u'builtins', 'zip', node)
