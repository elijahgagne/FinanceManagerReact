#!/bin/bash

WORKERS=${WORKERS:-4}

# For Production
#export GUNICORN_ARGS="--limit-request-line 65536 --limit-request-field_size 65536"

# For Development
#export GUNICORN_ARGS="--reload"

gunicorn \
  --access-logfile - \
  --access-logformat '%({X-Forwarded-For}i)s %(h)s %(l)s %(u)s %(t)s "%(r)s" "%(f)s" "%(a)s" %(s)s %(b)s %(D)s' \
  --error-logfile - \
  --timeout 60 \
  --log-level=info \
  $GUNICORN_ARGS \
  --workers $WORKERS \
  --forwarded-allow-ips '*' \
  -b 0.0.0.0:5000 \
  api:api