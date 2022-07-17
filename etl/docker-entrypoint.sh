#!/bin/sh
./wait-for-it.sh postgres:5432 -t 15 -- echo "postgres is up"
./wait-for-it.sh es:9200 -t 15 -- echo "elasticsearch is up"
./wait-for-it.sh service:8000 -t 15 -- echo "service is up"
echo 'Run etl'
python3 etl.py
exec "$@"