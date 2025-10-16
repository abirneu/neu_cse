#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (this includes admin CSS/JS)
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate
