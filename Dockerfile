FROM debian:9
# This docker image has a copy of a wide array of Pythons installed
RUN apt-get update
RUN apt-get install --yes --no-install-recommends make build-essential zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libffi-dev liblzma-dev libssl1.0-dev 
RUN apt-get install --yes git vim
RUN apt-get install --yes python3-pip
ENV PYENV_ROOT=/opt/pyenv
RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash 
RUN echo export PATH="/opt/pyenv/bin:$PATH" >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
# venv 15.2.0 is the last to support Python 2.6.  Since the venv module of the installer 
RUN pip3 install virtualenv==15.2.0
RUN PATH=/opt/pyenv/bin:$PATH pyenv install 2.6.9
RUN virtualenv /opt/py26 --python /opt/pyenv/versions/2.6.9/bin/python
RUN PATH=/opt/pyenv/bin:$PATH pyenv install 3.3.7
RUN virtualenv /root/py33 --python /opt/pyenv/versions/3.3.7/bin/python
RUN pip3 install virtualenv==20.0.21
RUN PATH=/opt/pyenv/bin:$PATH pyenv install 3.4.10
RUN virtualenv /root/py34 --python /opt/pyenv/versions/3.4.10/bin/python
RUN apt-get install --yes libssl-dev libxmlsec1-dev
RUN PATH=/opt/pyenv/bin:$PATH pyenv install 2.7.18
RUN virtualenv /root/py27 --python /opt/pyenv/versions/2.7.18/bin/python
RUN PATH=/opt/pyenv/bin:$PATH pyenv install 3.5.9
RUN virtualenv /root/py35 --python /opt/pyenv/versions/3.5.9/bin/python
RUN PATH=/opt/pyenv/bin:$PATH pyenv install 3.6.10
RUN virtualenv /root/py36 --python /opt/pyenv/versions/3.6.10/bin/python
RUN PATH=/opt/pyenv/bin:$PATH pyenv install 3.7.7
RUN virtualenv /root/py37 --python /opt/pyenv/versions/3.7.7/bin/python
RUN PATH=/opt/pyenv/bin:$PATH pyenv install 3.8.3
RUN virtualenv /root/py38 --python /opt/pyenv/versions/3.8.3/bin/python
RUN PATH=/opt/pyenv/bin:$PATH pyenv install 3.9.0a6
RUN virtualenv /root/py39 --python /opt/pyenv/versions/3.9.0a6/bin/python
RUN ln -s /usr/bin/python3 /usr/bin/python
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
WORKDIR /root/python-future
ADD . /root/python-future
