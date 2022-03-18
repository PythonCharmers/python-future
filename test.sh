#!/bin/bash

set -exo pipefail

pip install pytest unittest2

python setup.py bdist_wheel
pip install dist/future-*-none-any.whl
pytest tests/
