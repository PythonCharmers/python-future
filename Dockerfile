ARG DEBIAN_VERSION
ARG PYTHON_VERSION
# Note: venv 15.2.0 is the last to support Python 2.6.
ARG VIRTUALENV_VERSION

FROM debian:${DEBIAN_VERSION}

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
    make \
    build-essential \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libffi-dev \
    liblzma-dev \
    libssl1.0-dev && \
    apt-get install --yes git vim && \
    apt-get install --yes python3-pip

ENV PYENV_ROOT=/opt/pyenv
RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash 
RUN echo export PATH="/opt/pyenv/bin:$PATH" >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

RUN pip3 install virtualenv==${VIRTUALENV_VERSION}

RUN PATH=/opt/pyenv/bin:$PATH pyenv install ${PYTHON_VERSION}
RUN virtualenv /root/venv --python /opt/pyenv/versions/${PYTHON_VERSION}/bin/python

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
WORKDIR /root/python-future
ADD . /root/python-future
