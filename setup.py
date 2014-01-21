#!/usr/bin/env python

import os
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import future


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

NAME = "future"
PACKAGES = ["future",
            "future.builtins",
            "future.builtins.backports",
            "future.tests",
            "future.standard_library",
            "future.standard_library.html",
            "future.standard_library.http",
            "future.standard_library.test",
            "future.utils",
            "libfuturize",
            "libfuturize.fixes2",
            "libfuturize.fixes3"]
PACKAGE_DATA = {'': [
                     'README.rst',
                     'LICENSE.txt',
                     'futurize.py',
                     'discover_tests.py',
                     'check_rst.sh'
                    ]}
REQUIRES = []
VERSION = future.__version__
DESCRIPTION = "Clean single-source support for Python 3 and 2"
LONG_DESC = future.__doc__
AUTHOR = "Ed Schofield"
AUTHOR_EMAIL = "ed@pythoncharmers.com"
URL="https://github.com/PythonCharmers/python-future"
LICENSE = "MIT"
KEYWORDS = "future python3 migration backport six 2to3 futurize modernize"
CLASSIFIERS = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "License :: OSI Approved",
    "License :: OSI Approved :: MIT License",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
]

setup_kwds = {}

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      description=DESCRIPTION,
      long_description=LONG_DESC,
      license=LICENSE,
      keywords=KEYWORDS,
      entry_points={
          'console_scripts': [
              'futurize = libfuturize.main:main'
          ]
      },
      packages=PACKAGES,
      package_data=PACKAGE_DATA,
      include_package_data=True,
      install_requires=REQUIRES,
      classifiers=CLASSIFIERS,
      test_suite = "discover_tests",
      **setup_kwds
     )

