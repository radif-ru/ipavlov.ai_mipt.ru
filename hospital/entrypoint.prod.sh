#!/bin/sh

gunicorn hospital.wsgi:application -b 0.0.0.0:8000 --reload
