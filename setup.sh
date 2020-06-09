#!/bin/bash

set -exo pipefail

version=$1
pytag=$2

if [ $pytag = 'py33' ]; then
    pip install virtualenv==16.2.0
fi

source /root/$pytag/bin/activate

if [ $pytag = 'py26' ]; then
    pip install importlib
fi
pip install pytest unittest2
python setup.py bdist_wheel --python-tag=$pytag
pip install dist/future-$version-$pytag-none-any.whl
pytest tests/
python setup.py clean
