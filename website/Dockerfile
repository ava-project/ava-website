FROM python:3.6.1-alpine

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install -r requirements.txt\
  && apk del build-deps

ADD . /app

ENV PYTHONUNBUFFERED 1

VOLUME /data

CMD ./entrypoints/dev.sh
