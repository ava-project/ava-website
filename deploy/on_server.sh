#!/usr/bin/env bash

set -e

# This script get the latest change and redeploy
cd `dirname $0`
cd ..
git pull
make build
