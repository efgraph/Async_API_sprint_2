FROM python:3.10

ENV REDIS_HOST=cache
ENV REDIS_PORT=6379

ENV API_URL=http://nginx/
ENV API_PATH=api/v1/

ENV ELASTIC_HOST=http://es
ENV ELASTIC_PORT=9200

ENV PYTHONPATH="${PYTHONPATH}:/opt/tests/src/"

WORKDIR /opt/tests

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .


