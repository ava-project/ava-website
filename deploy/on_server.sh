#!/usr/bin/env bash

set -e

# This script get the latest change and redeploy
cd `dirname $0`
cd ..


# add envs
export COMPOSE_FILE='docker-compose.prod.yml'

git pull
make deploy
