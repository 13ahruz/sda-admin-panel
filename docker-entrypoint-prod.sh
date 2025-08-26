#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Database is unavailable - sleeping"
  sleep 1
done
echo "Database is ready!"

# Run Django migrations for built-in apps (auth, admin, sessions, etc.)
echo "Running Django migrations for built-in apps..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Checking for admin user..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@sda.com', 'admin123')
    print('Admin user created: username=admin, password=admin123')
    print('IMPORTANT: Change the password after first login!')
else:
    print('Admin user already exists')
EOF

# Start Gunicorn
echo "Starting Django admin panel with Gunicorn..."
gunicorn sda_admin.wsgi:application \
    --bind 0.0.0.0:8001 \
    --workers 3 \
    --worker-class gthread \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
