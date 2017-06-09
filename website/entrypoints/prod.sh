#!/usr/bin/env sh

gunicorn --bind 0.0.0.0:8000 core.wsgi:application
