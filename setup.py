#!/usr/bin/env python

import os
import os.path
import sys

import future
import future.moves         # to allow running this script in the python-future source folder
from future.standard_library import exclude_local_folder_imports


with exclude_local_folder_imports('configparser'):
    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


NAME = "future"
PACKAGES = ["future",
            "future.builtins",
            "future.types",
            "future.standard_library",
            "future.backports",
            "future.backports.email",
            "future.backports.email.mime",
            "future.backports.html",
            "future.backports.http",
            "future.backports.test",
            "future.backports.urllib",
            "future.backports.xmlrpc",
            "future.moves",
            "future.moves.dbm",
            "future.moves.html",
            "future.moves.http",
            "future.moves.test",
            "future.moves.tkinter",
            "future.moves.urllib",
            "future.moves.xmlrpc",
            "future.tests",
            # "future.tests.test_email",
            "future.utils",
            "past",
            "past.builtins",
            "past.types",
            "past.utils",
            "past.tests",
            "past.translation",
            "libfuturize",
            "libfuturize.fixes",
            "libpasteurize",
            "libpasteurize.fixes",
           ]

# PEP 3108 stdlib moves:
if sys.version_info[:2] < (3, 0):
    PACKAGES += [
            "builtins",
            "configparser",
            "copyreg",
            "html",
            "http",
            "queue",
            "reprlib",
            "socketserver",
            "tkinter",
            "winreg",
            "xmlrpc",
            "_dummy_thread",
            "_markupbase",
            "_thread",
           ]

PACKAGE_DATA = {'': [
                     'README.rst',
                     'LICENSE.txt',
                     'futurize.py',
                     'pasteurize.py',
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
KEYWORDS = "future python3 migration backport six 2to3 futurize modernize past pasteurize"
CLASSIFIERS = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
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
              'futurize = libfuturize.main:main',
              'pasteurize = libpasteurize.main:main'
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
