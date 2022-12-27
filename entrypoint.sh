#!/bin/bash

python /app/manage.py collectstatic --no-input
python /app/manage.py migrate
# for create a first superuser. after this user should have a change a password
python /app/manage.py create_base_superuser
daphne ProductDate.wsgi:application -b 0.0.0.0 -p 8000
