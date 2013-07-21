
import sys
setup_kwds = {}

from distutils.core import setup

import future

NAME = "future"
PACKAGES = ["future", "future.features", "future.tests"]
VERSION = future.__version__
DESCRIPTION = "[experimental] support Python 2 with fewer warts"
LONG_DESC = future.__doc__
AUTHOR = "Ed Schofield"
AUTHOR_EMAIL = "ed@pythoncharmers.com"
URL="http://github.com/edschofield/python-future"
LICENSE = "MIT"
KEYWORDS = "future python3 migration backport"
CLASSIFIERS = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved",
    "License :: OSI Approved :: MIT License",
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
]

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      description=DESCRIPTION,
      long_description=LONG_DESC,
      license=LICENSE,
      keywords=KEYWORDS,
      packages=PACKAGES,
      classifiers=CLASSIFIERS,
      **setup_kwds
     )

