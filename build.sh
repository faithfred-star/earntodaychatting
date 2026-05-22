#!/usr/bin/env bash
# exit on error
set -o errexit

# Install required packages
pip install -r requirements.txt

# Collect static files (if you have static assets configured)
python manage.py collectstatic --no-input

# Run migrations automatically to fix the missing column column error
python manage.py migrate