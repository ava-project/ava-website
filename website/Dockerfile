FROM python:latest

RUN mkdir /app
WORKDIR /app

ADD requirement.txt /app
RUN pip install -r requirement.txt

ADD . /app

ENV PYTHONUNBUFFERED 1

CMD ./dev.sh
