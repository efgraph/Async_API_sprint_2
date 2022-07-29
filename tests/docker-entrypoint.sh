#!/bin/bash

echo "Waiting for cache is OK"
python src/utils/cache_check.py

echo "Waiting for API is OK"
python src/utils/api_check.py

echo "Waiting for Elastic is OK"
python src/utils/elastic_check.py

pytest