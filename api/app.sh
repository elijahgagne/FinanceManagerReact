#!/bin/bash
WORKERS=${WORKERS:-4}

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
