#!/bin/sh

export SECRET_KEY='django-insecure-(cm@&s^e_@3@wfu&wvm@o%laobyaw502miw5+g^hlz++1#ekm='
export DEBUG=Falses

python manage.py migrate --no-input
python manage.py collectstatic --no-input

/etc/init.d/nginx restart

celery -A config worker -l info

gunicorn config.wsgi:application --bind 0.0.0.0:8080
