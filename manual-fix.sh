#!/bin/bash

echo "=== Manual Django Tables Fix ==="
echo "This script manually creates Django tables if the automatic fix fails"
echo ""

# Check if container is running
if ! docker-compose -f docker-compose.simple.yml ps | grep -q "Up"; then
    echo "Starting admin panel container..."
    docker-compose -f docker-compose.simple.yml up -d
    sleep 10
fi

echo "Running manual migrations inside container..."

# Run each migration separately
echo "1. Migrating auth app..."
docker-compose -f docker-compose.simple.yml exec sda-admin python manage.py migrate auth

echo "2. Migrating contenttypes app..."
docker-compose -f docker-compose.simple.yml exec sda-admin python manage.py migrate contenttypes

echo "3. Migrating sessions app..."
docker-compose -f docker-compose.simple.yml exec sda-admin python manage.py migrate sessions

echo "4. Migrating admin app..."
docker-compose -f docker-compose.simple.yml exec sda-admin python manage.py migrate admin

echo "5. Migrating messages app..."
docker-compose -f docker-compose.simple.yml exec sda-admin python manage.py migrate messages

echo "6. Creating admin user..."
docker-compose -f docker-compose.simple.yml exec sda-admin python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@sda.com', 'admin123')
    print('Admin user created: username=admin, password=admin123')
else:
    print('Admin user already exists')
"

echo "7. Restarting container..."
docker-compose -f docker-compose.simple.yml restart sda-admin

echo ""
echo "=== Manual Fix Complete ==="
echo "Check if the admin panel works now: http://your-server-ip:8001/admin/"
