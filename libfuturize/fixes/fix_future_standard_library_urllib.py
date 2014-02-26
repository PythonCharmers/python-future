"""
For the ``future`` package.

A special fixer that ensures that these lines have been added::

    from future import standard_library
    standard_library.install_hooks()

even if the only module imported was ``urllib``, in which case the regular fixer
wouldn't have added these lines.

"""

from lib2to3.fixes.fix_urllib import FixUrllib
from libfuturize.fixer_util import touch_import_top


class FixFutureStandardLibraryUrllib(FixUrllib):     # not a subclass of FixImports
    run_order = 8

    def transform(self, node, results):
        result = super(FixFutureStandardLibraryUrllib, self).transform(node, results)
        # TODO: add a blank line between any __future__ imports and this?
        touch_import_top(u'future', u'standard_library', node)
        return result


