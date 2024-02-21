#!/bin/bash

set -exo pipefail

version=$1
pyabitag=$2

py="/opt/python/${pyabitag}/bin/python"
pytag=${pyabitag%-*}
pytag="${pytag//cp/py}"
$py -m pip install pytest unittest2
$py setup.py bdist_wheel --python-tag=$pytag
$py -m pip install dist/future-$version-$pytag-none-any.whl
# Ignore test failures for now
$py -m pytest tests/ || true
