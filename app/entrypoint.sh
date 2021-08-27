#!/bin/sh

# default to development mode
PRODUCTION=false

for arg; do
  if [[ $arg == "--production" ]]; then
    PRODUCTION=true
  fi
done

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py createsuperuser --noinput
if [[ $PRODUCTION == true ]]; then
  echo "Starting App in production mode..."
  python manage.py collectstatic --no-input --clear
  gunicorn app.wsgi:application --bind 0.0.0.0:8000
else
  echo "Starting app in development mode..."
  python manage.py runserver 0.0.0.0:8000
fi
