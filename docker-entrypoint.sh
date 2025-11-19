#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
until PGPASSWORD=${DB_PASSWORD} psql -h "${DB_HOST}" -U "${DB_USER}" -d "${DB_NAME}" -c '\q'; do
  >&2 echo "Database is unavailable - sleeping"
  sleep 1
done
echo "Database is ready!"

# Run Django migrations (tables already exist from backend, so fake them)
echo "Running Django migrations..."
python manage.py migrate --fake-initial
echo "Django migrations completed!"

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

# Start the Django development server
echo "Starting Django admin panel..."
python manage.py runserver 0.0.0.0:8001
