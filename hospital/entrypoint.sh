#! /bin/bash

gunicorn medical_institution.wsgi:application -b 0.0.0.0:8000 --reload
