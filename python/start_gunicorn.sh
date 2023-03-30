#!/bin/bash

echo Starting Gunicorn...
gunicorn entry_task.server.wsgi:application -c ./gunicorn.conf.py
