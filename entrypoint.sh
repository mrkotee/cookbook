#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# flush db and fill with test data
python manage.py flush --no-input
python manage.py makemigrations recipes
python manage.py migrate
python manage.py collectstatic
#python manage.py parse_recipes
python manage.py loaddata recipes_models

exec "$@"
