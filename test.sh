#!/bin/bash

set -exo pipefail

source /root/venv/bin/activate

if [ $pytag = 'py26' ]; then
    pip install importlib
fi
pip install pytest unittest2

python setup.py bdist_wheel
pip install dist/future-*-none-any.whl
pytest tests/
