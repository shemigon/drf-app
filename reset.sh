#!/usr/bin/env bash

set -e

if [ ! -f env ]; then
  if [ x$1 == x ]; then
    echo "$0 [<python3.{6,7}>]"
    echo "  pathon executable to use in the virtual environvent if it's not exists"
    exit 2
  fi
  virtualenv env -p$1
  env/bin/pip install -r requirements.txt
fi

[ -f db.sqlite3 ] && rm db.sqlite3

. env/bin/activate

./manage.py migrate
./manage.py loaddata initial.json
