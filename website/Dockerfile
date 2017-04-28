FROM python:3.6.1

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app

ENV PYTHONUNBUFFERED 1

VOLUME /data

CMD ./entrypoints/dev.sh
