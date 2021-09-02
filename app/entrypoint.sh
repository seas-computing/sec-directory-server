#!/bin/sh

# default to development mode
EXEC_MODE=exec

if [[ "$*" == "--production" ]]; then
  EXEC_MODE=production
elif [[ "$*" == "--development" ]]; then
  EXEC_MODE=development
fi

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

if [[ $EXEC_MODE == exec ]]; then
  echo "Running $@"
  exec "$@"
else
  python manage.py migrate
  python manage.py createsuperuser --noinput
  if [[ $EXEC_MODE == development ]]; then
    echo "Starting app in development mode..."
    python manage.py runserver 0.0.0.0:8000
  elif [[ $EXEC_MODE == production ]]; then
    echo "Starting App in production mode..."
    gunicorn app.wsgi:application --bind 0.0.0.0:8000
  fi
fi
