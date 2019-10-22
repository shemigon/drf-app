#!/usr/bin/env bash

[ -f db.sqlite3 ] && rm db.sqlite3

. env/bin/activate

./manage.py migrate
./manage.py shell -c "from drfapp.core.models import User; User.objects.create_superuser('root@localhost', '123')"
./manage.py shell -c "from django.contrib.auth.models import Group;Group.objects.bulk_create([Group(name='Administrator'),Group(name='Viewer'),Group(name='User')])"
