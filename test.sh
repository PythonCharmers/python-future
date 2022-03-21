#!/bin/bash

if [ -e "${HOME}/.bashrc" ]
then
  source "${HOME}/.bashrc"
fi

set -exo pipefail

python --version

if [ -e "/root/pip" ]
then
  pip install /root/pip/*.zip /root/pip/*.whl /root/pip/*tar.gz
else
  pip install pytest unittest2
fi

pytag="py${PYTHON_VERSION//./}"

python setup.py bdist_wheel --python-tag="${pytag}"
pip install dist/future-*-${pytag}-none-any.whl
pytest tests/
