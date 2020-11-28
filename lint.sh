# TODO: Run under Python 2.7 and 3.7
flake8 . --count --exit-zero --select=E901,E999,F821,F822,F823 --show-source --statistics || true
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics || true
