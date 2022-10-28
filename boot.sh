#!/bin/bash
source venv/bin/activate
flask db upgrade

exec gunicorn -b :5000 -w 4 --access-logfile - --error-logfile - randomThought:app