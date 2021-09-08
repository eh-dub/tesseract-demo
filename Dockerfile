FROM python:3.9-slim

RUN pip install --user poetry
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /tesseract-demo