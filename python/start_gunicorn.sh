#!/bin/bash

echo Starting Gunicorn...
gunicorn entry_task.server.wsgi:application -c ./gunicorn.conf.py --bind 127.0.0.1:8000
