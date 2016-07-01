FROM python:latest

RUN apt-get update ; apt-get upgrade -y
RUN apt-get install libmysqlclient-dev

# RUN mkdir /scripts
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/bin
RUN mv /usr/bin/wait-for-it.sh /usr/bin/wait-for-it
RUN chmod 755 /usr/bin/wait-for-it

RUN mkdir /app
WORKDIR /app

ADD requirement.txt .
RUN pip install -r requirement.txt

CMD ./start.sh
