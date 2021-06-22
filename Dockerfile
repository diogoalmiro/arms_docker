FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install tesseract-ocr -y \
    python3 \
    #python-setuptools \
    python3-pip \
    libtesseract-dev \
    libleptonica-dev \
    pkg-config \
    ffmpeg \
    libsm6 \
    libxext6  -y \
    && apt-get clean \
    && apt-get autoremove

ADD workflow /home/App
WORKDIR /home/App
COPY requirements.txt ./

RUN apt-get install libffi-dev -y
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
