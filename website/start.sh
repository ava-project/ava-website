#!/usr/bin/env bash

# wait for database
while ! curl http://db:3306/ > /dev/null 2> /dev/null
do
  echo "$(date) - Waiting for mysql"
  sleep 1
done
echo "$(date) - mysql is up !"

python manage.py migrate

while true
do
    python3 -u manage.py runserver 0.0.0.0:8000
    sleep 1
done
