FROM python:3.6.1-alpine

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install -r requirements.txt\
  && curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash\
  && apk del build-deps gcc musl-dev python3-dev

ADD . /app

ENV PYTHONUNBUFFERED 1


CMD ./entrypoints/dev.sh
