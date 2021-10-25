#!/usr/bin/env sh
set -ex

cd /app

if [ $# -eq 0 ]; then
    echo "Usage: start.sh [PROCESS_TYPE](server/beat/worker/flower)"
    exit 1
fi

PROCESS_TYPE=$1

if [ "$PROCESS_TYPE" = "server" ]; then
  # --worker-class eventlet \
    gunicorn \
        --bind 0.0.0.0:8000 \
        --workers 4 \
        --timeout 90 \
        --log-level ${LOG_LEVEL:-DEBUG} \
        --access-logfile "-" \
        --error-logfile "-" \
        config.wsgi
elif [ "$PROCESS_TYPE" = "beat" ]; then
    celery \
        --app config.celery_app \
        beat \
        --loglevel ${CELERY_LOG_LEVEL:-INFO} \
        --scheduler django_celery_beat.schedulers:DatabaseScheduler
elif [ "$PROCESS_TYPE" = "flower" ]; then
    celery \
        --app config.celery_app \
        flower \
        --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}" \
        --loglevel ${CELERY_LOG_LEVEL:-INFO}
elif [ "$PROCESS_TYPE" = "worker" ]; then
    celery \
        --app config.celery_app \
        worker \
        --soft-time-limit=900 \
        --time-limit=900 \
        --loglevel ${CELERY_LOG_LEVEL:-INFO}
fi
