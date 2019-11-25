#!/bin/sh
gunicorn access_check.wsgi --bind 127.0.0.1:8080 --workers 5 --threads 4 --max-requests-jitter 10000 --max-requests 1000000 --keep-alive 32