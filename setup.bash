#!/usr/bin/env bash

if [ ! -x $(which virtualenv) ]; then
  pip install virtualenv
fi

if [ ! -x $(which aws) ]; then
  pip install awscli
fi

if [ ! -d .env ]; then
  virtualenv --no-site-packages --distribute .env
fi

source .env/bin/activate
pip install -U requirements.txt
