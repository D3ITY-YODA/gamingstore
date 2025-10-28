#!/bin/bash

# Create static files directory
mkdir -p staticfiles

# Collect static files
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

# Apply database migrations
echo "=== Running database migrations ==="
python manage.py migrate

# Create superuser if not exists (optional - you can do this manually)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell

echo "=== Starting Gunicorn ==="
# Start Gunicorn
gunicorn store.wsgi:application --bind 0.0.0.0:8000 --workers 2
