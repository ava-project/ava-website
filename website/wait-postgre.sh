#!/usr/bin/env bash

set -e

until nc -vz "db" 5432; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is available"
