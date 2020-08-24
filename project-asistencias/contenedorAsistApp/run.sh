#!/bin/bash

sleep 15

su -c 'python3 -u /monitor/monitor.py &' restringido

su -c 'python3 -u manage.py makemigrations' restringido
su -c 'python3 -u manage.py migrate' restringido
su -c 'gunicorn --bind :8000 Asistencias.wsgi:application --reload' restringido