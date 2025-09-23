#!/usr/bin/env bash
# build.sh
set -o errexit # Exit on any error

# Install Python dependencies
pip install -r requirements.txt

# Collect static files (important for Render)
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Note: Render will run the start command separately (e.g., gunicorn)