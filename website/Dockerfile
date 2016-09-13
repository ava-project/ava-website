FROM python:latest

RUN apt-get update ; apt-get upgrade -y
RUN apt-get install libmysqlclient-dev

RUN mkdir /app
WORKDIR /app

ADD requirement.txt .
RUN pip install -r requirement.txt

ENV PYTHONUNBUFFERED 1

CMD ./start.sh
