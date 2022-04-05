#!/bin/sh

# default to development mode
EXEC_MODE=exec

if [[ "$*" == "--production" ]]; then
  EXEC_MODE=production
elif [[ "$*" == "--development" ]]; then
  EXEC_MODE=development
elif [[ "$*" == "--reindex" ]]; then
  EXEC_MODE=reindex
fi

# Default to SERVER_PORT 8000
if [[ -z "$SERVER_PORT" ]]; then
  SERVER_PORT=8000
fi

# Attempt to connect to the postgres port, bailing after two minutes
if [[ $DATABASE == postgres ]]
then
  echo "Waiting for postgres..."

  let COUNT=0
  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 2
    let COUNT=$COUNT+1
    if [[ $COUNT -ge 60 ]]; then
      exit 1
    fi
  done

  echo "PostgreSQL started"
fi

if [[ $EXEC_MODE == exec ]]; then
  echo "Running $@"
  exec "$@"
elif [[ $EXEC_MODE == reindex ]]; then
  echo "Reindexing Database"
  python manage.py shell\
    --command="from feedperson.utils import load_feed_people;\
    load_feed_people()"
  python manage.py algolia_reindex
else
  python manage.py migrate
  python manage.py createsuperuser --noinput
  if [[ $EXEC_MODE == development ]]; then
    echo "Starting app in development mode..."
    python manage.py runserver 0.0.0.0:$SERVER_PORT
  elif [[ $EXEC_MODE == production ]]; then
    echo "Starting App in production mode..."
    gunicorn app.wsgi:application --bind 0.0.0.0:$SERVER_PORT
  fi
fi
