FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1
WORKDIR social_media/

COPY requirements.txt /social_media/
RUN python -m pip install -r requirements.txt

COPY . /social_media/
