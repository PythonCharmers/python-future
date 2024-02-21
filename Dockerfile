ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim

ENV LC_ALL=C.UTF-8

WORKDIR /root/python-future
ADD . /root/python-future
