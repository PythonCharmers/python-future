FROM mrupgrade/deadsnakes:2.6

RUN mkdir -p ~/.pip/ && echo '[global] \n\
trusted-host = pypi.python.org\n\
               pypi.org\n\
               files.pythonhosted.org\n\
' >> ~/.pip/pip.conf

RUN apt-get update && \
    apt-get install -y curl

RUN mkdir -p /root/pip && \
    cd /root/pip && \
    curl -O https://files.pythonhosted.org/packages/8a/e9/8468cd68b582b06ef554be0b96b59f59779627131aad48f8a5bce4b13450/wheel-0.29.0-py2.py3-none-any.whl && \
    curl -O https://files.pythonhosted.org/packages/31/77/3781f65cafe55480b56914def99022a5d2965a4bb269655c89ef2f1de3cd/importlib-1.0.4.zip && \
    curl -O https://files.pythonhosted.org/packages/ef/41/d8a61f1b2ba308e96b36106e95024977e30129355fd12087f23e4b9852a1/pytest-3.2.5-py2.py3-none-any.whl && \
    curl -O https://files.pythonhosted.org/packages/f2/94/3af39d34be01a24a6e65433d19e107099374224905f1e0cc6bbe1fd22a2f/argparse-1.4.0-py2.py3-none-any.whl && \
    curl -O https://files.pythonhosted.org/packages/72/20/7f0f433060a962200b7272b8c12ba90ef5b903e218174301d0abfd523813/unittest2-1.1.0-py2.py3-none-any.whl && \
    curl -O https://files.pythonhosted.org/packages/53/67/9620edf7803ab867b175e4fd23c7b8bd8eba11cb761514dcd2e726ef07da/py-1.4.34-py2.py3-none-any.whl && \
    curl -O https://files.pythonhosted.org/packages/53/25/ef88e8e45db141faa9598fbf7ad0062df8f50f881a36ed6a0073e1572126/ordereddict-1.1.tar.gz && \
    curl -O https://files.pythonhosted.org/packages/17/0a/6ac05a3723017a967193456a2efa0aa9ac4b51456891af1e2353bb9de21e/traceback2-1.4.0-py2.py3-none-any.whl && \
    curl -O https://files.pythonhosted.org/packages/65/26/32b8464df2a97e6dd1b656ed26b2c194606c16fe163c695a992b36c11cdf/six-1.13.0-py2.py3-none-any.whl && \
    curl -O https://files.pythonhosted.org/packages/c7/a3/c5da2a44c85bfbb6eebcfc1dde24933f8704441b98fdde6528f4831757a6/linecache2-1.0.0-py2.py3-none-any.whl

WORKDIR /root/python-future
ADD . /root/python-future