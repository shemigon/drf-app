#!/usr/bin/env bash

[ -f db.sqlite3 ] && rm db.sqlite3

. env/bin/activate

./manage.py migrate
./manage.py loaddata initial.json
