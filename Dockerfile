FROM python:3.6.8-alpine3.9

RUN apk add --update --no-cache build-base nginx openssl curl unzip supervisor jpeg-dev zlib-dev postgresql-dev freetype-dev && \
    pip install --no-cache-dir -r /app/deploy/requirements.txt && \
    apk del build-base --purge

ADD . /app

WORKDIR /app

RUN chmod +x /app/deploy/entrypoint.sh

ENTRYPOINT /app/deploy/entrypoint.sh