#!/usr/bin/env bash

python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 core.wsgi:application
