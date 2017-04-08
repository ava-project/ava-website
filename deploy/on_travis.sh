#!/usr/bin/env bash

set -e

# This script connect to the server and call the deploy script
curl $DEPLOY_URL\
  -X POST\
  -d '{"token": "'$DEPLOY_TOKEN'"}'\
  -H "Content-Type: application/json"
