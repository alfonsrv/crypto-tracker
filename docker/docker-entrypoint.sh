#!/usr/bin/env sh
set -ex
#set -o errexit
#set -o pipefail
#set -o nounset

until nc -w 1 -z db 5432; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
sleep 2
>&2 echo "Postgres is up - executing command"

until nc -w 1 -z redis 6379; do
  >&2 echo "REDIS is unavailable - sleeping"
  sleep 1
done
sleep 2
>&2 echo "REDIS is up - executing command"

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"
