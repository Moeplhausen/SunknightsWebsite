#!/bin/bash

# we need to install pip first

pip3 install -r requirements.txt --user
python3 manage.py migrate
python3 manage.py loaddata fixture.json
