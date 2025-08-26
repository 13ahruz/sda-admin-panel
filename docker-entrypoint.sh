#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Database is unavailable - sleeping"
  sleep 1
done
echo "Database is ready!"

# Run Django migrations for built-in apps only (auth, admin, sessions, etc.)
echo "Running Django migrations for built-in apps..."
python manage.py migrate auth
python manage.py migrate contenttypes
python manage.py migrate sessions  
python manage.py migrate admin
python manage.py migrate messages
echo "Django built-in tables created successfully!"

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
