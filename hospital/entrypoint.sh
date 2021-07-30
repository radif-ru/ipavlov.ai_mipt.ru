#! /bin/bash

python manage.py add_groups

gunicorn hospital.wsgi:application -b 0.0.0.0:8000 --reload
