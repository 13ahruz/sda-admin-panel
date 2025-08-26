#!/bin/bash

echo "Fixing Django tables and session issues..."

# Navigate to the admin panel directory
cd /path/to/your/admin-panel

# Run the fix script inside the Django container
docker-compose exec web python fix_django_tables.py

# If the above doesn't work, try running migrations manually
echo "Running Django migrations for built-in apps..."
docker-compose exec web python manage.py migrate auth
docker-compose exec web python manage.py migrate contenttypes  
docker-compose exec web python manage.py migrate sessions
docker-compose exec web python manage.py migrate admin

# Create admin user if needed
echo "Creating admin user..."
docker-compose exec web python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created! Username: admin, Password: admin123')
else:
    print('Admin user already exists.')
"

# Restart the web service to ensure everything is working
echo "Restarting web service..."
docker-compose restart web

echo "Django tables fix completed!"
echo "You can now access the admin panel with:"
echo "Username: admin"
echo "Password: admin123"
