#!/bin/sh
./wait-for-it.sh postgres:5432 -t 10 -- echo "postgres is up"
echo 'Run migration'
python3 manage.py migrate
python3 load_data.py
echo 'Create super user'
python3 manage.py createsuperuser --noinput
echo 'Collect Static'
python3 manage.py collectstatic --noinput
uwsgi --ini uwsgi.ini
exec "$@"