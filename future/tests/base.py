import os
import tempfile
import unittest
if not hasattr(unittest, 'skip'):
    import unittest2 as unittest

from textwrap import dedent
import subprocess

# For Python 2.6 compatibility: see http://stackoverflow.com/questions/4814970/
if "check_output" not in dir(subprocess): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

class CodeHandler(unittest.TestCase):
    """
    Handy mixin for test classes for writing / reading / futurizing /
    running .py files in the test suite.
    """
    def setUp(self):
        """
        The outputs from the various futurize stages should have the
        following headers:
        """
        # After stage1:
        # TODO: use this form after implementing a fixer to consolidate
        #       __future__ imports into a single line:
        # self.headers1 = """
        # from __future__ import absolute_import, division, print_function
        # """
        self.headers1 = self.reformat("""
        from __future__ import absolute_import
        from __future__ import division
        from __future__ import print_function
        """)

        # After stage2:
        # TODO: use this form after implementing a fixer to consolidate
        #       __future__ imports into a single line:
        # self.headers2 = """
        # from __future__ import (absolute_import, division,
        #                         print_function, unicode_literals)
        # from future import standard_library
        # from future.builtins import *
        # """
        self.headers2 = self.reformat("""
        from __future__ import absolute_import
        from __future__ import division
        from __future__ import print_function
        from __future__ import unicode_literals
        from future import standard_library
        from future.builtins import *
        """)
        self.interpreters = ['python']
        self.tempdir = tempfile.mkdtemp() + os.path.sep
        self.env = {'PYTHONPATH': os.getcwd()}

    def convert(self, code, stages=(1, 2), all_imports=False, from3=False,
                reformat=True, run=True):
        """
        Converts the code block using ``futurize`` and returns the
        resulting code.
        
        Passing stages=[1] or stages=[2] passes the flag ``--stage1`` or
        ``stage2`` to ``futurize``. Passing both stages runs ``futurize``
        with both stages by default.

        If from3 is False, runs ``futurize`` in the default mode,
        converting from Python 2 to both 2 and 3. If from3 is True, runs
        ``futurize --from3`` to convert from Python 3 to both 2 and 3.

        Optionally reformats the code block first using the reformat()
        method.

        If run is True, runs the resulting code under all Python
        interpreters in self.interpreters.
        """
        if reformat:
            code = self.reformat(code)
        self._write_test_script(code)
        self._futurize_test_script(stages=stages, all_imports=all_imports,
                                   from3=from3)
        output = self._read_test_script()
        if run:
            for interpreter in self.interpreters:
                _ = self._run_test_script(interpreter=interpreter)
        return output

    def reformat(self, code):
        """
        Removes any leading \n and dedents.
        """
        if code.startswith('\n'):
            code = code[1:]
        return dedent(code)

    def check(self, output, expected, ignore_imports=True):
        """
        Compares whether the code blocks are equal. If not, raises an
        exception so the test fails. Ignores any trailing whitespace like
        blank lines.

        If ignore_imports is True, passes the code blocks into the
        strip_future_imports method.
        """
        # self.assertEqual(expected.rstrip(),
        #                  self.order_future_lines(output).rstrip())
        if ignore_imports:
            output = self.strip_future_imports(output)
            expected = self.strip_future_imports(expected)
        self.assertEqual(self.order_future_lines(output.rstrip()),
                         expected.rstrip())

    def strip_future_imports(self, code):
        """
        Strips any of these import lines:

            from __future__ import <anything>
            from future <anything>
            from future.<anything>

        Limitation: doesn't handle imports split across multiple lines like
        this:

            from __future__ import (absolute_import, division, print_function,
                                    unicode_literals)
        """
        output = []
        for line in code.splitlines():
            if not (line.startswith('from __future__ import ')
                    or line.startswith('from future ')
                    # but don't match "from future_builtins" :)
                    or line.startswith('from future.')):
                output.append(line)
        return '\n'.join(output)

    def convert_check(self, before, expected, stages=(1, 2),
                      all_imports=False, ignore_imports=True, from3=False,
                      run=True):
        """
        Convenience method that calls convert() and check().

        Reformats the code blocks automatically using the reformat()
        method.

        If all_imports is passed, we add the appropriate import headers
        for the stage(s) selected to the ``expected`` code-block, so they
        needn't appear repeatedly in the test code.

        If ignore_imports is True, ignores the presence of any lines
        beginning:
        
            from __future__ import ...
            from future import ...
            
        for the purpose of the comparison.
        """
        output = self.convert(before, stages=stages,
                              all_imports=all_imports, from3=from3,
                              run=run)
        if all_imports:
            headers = self.headers2 if 2 in stages else self.headers1
        else:
            headers = ''

        self.check(output, self.reformat(headers + expected),
                   ignore_imports=ignore_imports)

    def check_old(self, output, expected, stages=(1, 2), ignore_imports=True):
        """
        Checks that the output is equal to the expected output, after
        reformatting.
        
        Pass ``expected`` as a string (as a code block). It will be
        reformatted and compared with the resulting code. We assert that
        the output of the conversion of ``before`` with ``futurize`` is
        equal to ``after``. Unless ignore_imports is True, the
        appropriate headers for the stage(s) used are added automatically
        for the comparison.
        """
        headers = ''
        # if not ignore_imports:
        #     if 2 in stages:
        #         headers = self.headers2
        #     else:
        #         headers = self.headers1
        self.compare(output, headers + self.reformat(expected),
                     ignore_imports=ignore_imports)

    def order_future_lines(self, code):
        """
        TODO: simplify this hideous code ...

        Returns the code block with any ``__future__`` import lines sorted, and
        then any ``future`` import lines sorted.
        """
        codelines = code.splitlines()
        # Under under future lines:
        uufuture_line_numbers = [i for i in range(len(codelines)) if codelines[i].startswith('from __future__ import ')]
        sorted_uufuture_lines = sorted([codelines[i] for i in uufuture_line_numbers])

        # future import lines:
        future_line_numbers = [i for i in range(len(codelines)) if codelines[i].startswith('from future')]
        sorted_future_lines = sorted([codelines[i] for i in future_line_numbers])

        # Replace the old unsorted "from __future__ import ..." lines with the
        # new sorted ones:
        codelines2 = []
        for i in range(len(codelines)):
            if i in uufuture_line_numbers:
                codelines2.append(sorted_uufuture_lines[i])
            elif i in future_line_numbers:
                codelines2.append(sorted_future_lines[i - len(uufuture_line_numbers)])
            else:
                codelines2.append(codelines[i])
        return '\n'.join(codelines2)

    def unchanged(self, code, **kwargs):
        """
        Convenience method to ensure the code is unchanged by the
        futurize process.
        """
        self.convert_check(code, code, **kwargs)

    def _write_test_script(self, code, filename='mytestscript.py'):
        """
        Dedents the given code (a multiline string) and writes it out to
        a file in a temporary folder like /tmp/tmpUDCn7x/mytestscript.py.
        """
        with open(self.tempdir + filename, 'w') as f:
            f.write(dedent(code))

    def _read_test_script(self, filename='mytestscript.py'):
        with open(self.tempdir + filename) as f:
            newsource = f.read()
        return newsource

    def _futurize_test_script(self, filename='mytestscript.py', stages=(1, 2),
                              all_imports=False, from3=False):
        params = []
        stages = list(stages)
        if all_imports:
            params.append('--all-imports')
        if from3:
            params.append('--from3')
        if stages == [1]:
            params.append('--stage1')
        elif stages == [2]:
            params.append('--stage2')
        else:
            assert stages == [1, 2]
            # No extra params needed

        output = subprocess.check_output(['python', 'futurize.py'] + params +
                                         ['-w', self.tempdir + filename],
                                         stderr=subprocess.STDOUT)
        return output

    def _run_test_script(self, filename='mytestscript.py',
                         interpreter='python'):
        env = {'PYTHONPATH': os.getcwd()}
        return subprocess.check_output([interpreter, self.tempdir + filename],
                                       env=env)


