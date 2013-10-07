import os
import tempfile
from unittest import TestCase
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
            raise CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

class CodeHandler(TestCase):
    """
    Handy mixin for test classes for writing / reading / futurizing /
    running .py files in the test suite.
    """
    def setUp(self):
        """
        The outputs from the various futurize stages should have the following
        headers:
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

    def simple_convert(self, code, stages=(1, 2), from3=False):
        """
        Returns the equivalent of ``code`` after passing it to the ``futurize``
        script.
        """
        self._write_test_script(code)
        self._futurize_test_script(stages=stages, from3=from3)
        return self._read_test_script()

    def reformat(self, code):
        """
        Removes any leading \n and dedents.
        """
        if code.startswith('\n'):
            code = code[1:]
        return dedent(code)

    def compare(self, output, expected):
        """
        Compares whether the code blocks are equal. Ignores the order of
        __future__ and future import lines and any trailing whitespace like
        blank lines.
        """
        self.assertEqual(expected.rstrip(),
                         self.order_future_lines(output).rstrip())

    def convert_check(self, before, expected=None, stages=(1, 2), from3=False, run=True):
        """
        Reformats the ``before`` code block, converts it using ``futurize``
        and, optionally, and runs the resulting code.
        
        If run is True, runs the resulting code under all Python interpreters
        in self.interpreters.

        If ``expected`` is passed (as a code block), it is reformatted and
        compared with the resulting code. If ``expected`` is passed, we assert
        that the output of the conversion of ``before`` with ``futurize`` is
        equal to ``after`` plus the appropriate headers (self.headers1 or
        self.headers2) depending on the stage(s) used.

        Passing stages=[1] or stages=[2] passes the flag ``--stage1`` or
        ``stage2`` to ``futurize``. Passing both stages runs ``futurize`` with
        both stages by default.

        If from3 is False, runs ``futurize`` in the default mode, converting
        from Python 2 to both 2 and 3. If from3 is True, runs ``futurize
        --from3`` to convert from Python 3 to both 2 and 3.
        """
        output = self.simple_convert(self.reformat(before), stages=stages, from3=from3)
        if run:
            for interpreter in self.interpreters:
                _ = self._run_test_script(interpreter=interpreter)

        if expected is not None:
            if 2 in stages:
                headers = self.headers2
            else:
                headers = self.headers1
            self.compare(output, headers + self.reformat(expected))

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

    def unchanged(self, code, stages=(1, 2), from3=False, run=True):
        """
        Tests to ensure the code is unchanged by the futurize process,
        exception for the addition of __future__ and future imports.
        """
        self.convert_check(code, code, stages, from3, run)

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

    def _futurize_test_script(self, filename='mytestscript.py', stages=(1, 2), from3=False):
        params = []
        stages = list(stages)
        if from3:
            params += ['--from3']
        if stages == [1]:
            params += ['--stage1']
        elif stages == [2]:
            params += ['--stage2']
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


