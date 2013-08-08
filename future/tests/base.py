import os
import textwrap
from subprocess import check_output, STDOUT


class CodeHandler(object):
    """
    Handy mixin for test classes for writing / reading / futurizing /
    running .py files in the test suite.
    """
    def _write_test_script(self, code, filename='mytestscript.py'):
        """
        Dedents the given code (a multiline string) and writes it out to
        a file in a temporary folder like /tmp/tmpUDCn7x/mytestscript.py.
        """
        with open(self.tempdir + filename, 'w') as f:
            f.write(textwrap.dedent(code))

    def _read_test_script(self, filename='mytestscript.py'):
        with open(self.tempdir + filename) as f:
            newsource = f.read()
        return newsource

    def _futurize_test_script(self, filename='mytestscript.py'):
        output = check_output(['python', 'futurize.py', '-w',
                               self.tempdir + filename],
                              stderr=STDOUT)
        print(output)
        return output

    def _run_test_script(self, filename='mytestscript.py'):
        env = {'PYTHONPATH': os.getcwd()}
        return check_output([self.interpreter, self.tempdir + filename],
                            env=env)


