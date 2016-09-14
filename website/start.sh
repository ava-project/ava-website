#!/usr/bin/env bash

while true
do
    python3 -u manage.py runserver 0.0.0.0:8000
    sleep 1
done
