FROM python:latest

RUN apt-get update ; apt-get upgrade -y
RUN apt-get install libmysqlclient-dev

# RUN apt-get install python-docutils -y
# RUN apt-get install rst2pdf -y

RUN mkdir /app
WORKDIR /app

ADD requirement.txt .
RUN pip install -r requirement.txt

ENV PYTHONUNBUFFERED 1

CMD ./start.sh
