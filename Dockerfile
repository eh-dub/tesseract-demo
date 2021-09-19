FROM python:3.9-slim

#Install MINICONDA
RUN apt-get update && apt-get install -y wget && wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda.sh && \
    /bin/bash Miniconda.sh -b -p /opt/conda 

ENV PATH /opt/conda/bin:$PATH

WORKDIR /tesseract

COPY environment.yml ./

RUN conda env create -f environment.yml
