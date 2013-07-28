"""
Example Python 3 code using the new urllib.request module.

Does libfuturize handle this?
"""
URL = 'http://pypi.python.org/pypi/{}/json'

package = 'future'

import pprint
# import requests
# 
# r = requests.get(URL.format(package))
# pprint.pprint(r.json())

import urllib.request
r = urllib.request.urlopen(URL.format(package_name))
pprint.pprint(r.read())
