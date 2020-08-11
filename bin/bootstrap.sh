#!/usr/bin/env sh

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py makemigrations core
./manage.py migrate
./manage.py loaddata core/fixtures/cities.json
