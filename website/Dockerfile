FROM python:latest

RUN apt-get update -y ; apt-get upgrade -y
RUN apt-get install netcat -y

RUN mkdir /app
WORKDIR /app

ADD requirement.txt .
RUN pip install -r requirement.txt

ENV PYTHONUNBUFFERED 1

CMD ./start.sh
