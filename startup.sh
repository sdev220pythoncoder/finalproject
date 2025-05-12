#!/bin/bash
source venv/bin/activate
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn snowboard_shop.wsgi --bind=0.0.0.0:8000 --timeout 600
