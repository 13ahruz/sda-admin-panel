#!/bin/bash

echo "=== SDA Admin Panel Django Tables Fix ==="
echo "This script will fix the Django session table issue"
echo ""

# Stop the current containers
echo "1. Stopping current containers..."
docker-compose -f docker-compose.simple.yml down

# Rebuild the image with the updated entrypoint
echo "2. Rebuilding admin panel with fixes..."
docker-compose -f docker-compose.simple.yml build --no-cache

# Start the containers
echo "3. Starting admin panel..."
docker-compose -f docker-compose.simple.yml up -d

# Wait a moment for the container to start
echo "4. Waiting for container to start..."
sleep 10

# Check the logs
echo "5. Checking container logs..."
docker-compose -f docker-compose.simple.yml logs sda-admin

echo ""
echo "=== Fix Complete ==="
echo "Admin panel should now be accessible at: http://your-server-ip:8001/admin/"
echo "Default login credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "IMPORTANT: Change the admin password after first login!"
echo ""
echo "If you still see errors, run:"
echo "docker-compose -f docker-compose.simple.yml logs sda-admin"
