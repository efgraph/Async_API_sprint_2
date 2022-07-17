FROM nikolaik/python-nodejs

WORKDIR /opt/etl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN npm install -g newman

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /opt/etl/docker-entrypoint.sh
RUN chmod +x /opt/etl/wait-for-it.sh

EXPOSE 8000
