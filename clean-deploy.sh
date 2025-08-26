#!/bin/bash

echo "=== SDA Admin Panel - Clean Migration Issues ==="
echo "This script fixes migration conflicts and deploys a clean admin panel"
echo ""

# Stop any running admin panel
echo "1. Stopping existing admin panel..."
docker stop sda-admin-panel 2>/dev/null || true
docker rm sda-admin-panel 2>/dev/null || true

# Clear any Django migration history for our app in the database
echo "2. Clearing Django migration history for sda_models..."
docker exec sda_db_1 psql -U postgres -d sda_db -c "DELETE FROM django_migrations WHERE app = 'sda_models';" 2>/dev/null || echo "No migration records to clear"

# Build fresh image
echo "3. Building fresh admin panel image..."
docker build -t sda-admin-panel . --no-cache

# Start with clean state
echo "4. Starting admin panel with clean migration state..."
SDA_NETWORK=$(docker inspect sda_db_1 2>/dev/null | grep -o '"NetworkMode": "[^"]*"' | cut -d'"' -f4)
if [ ! -z "$SDA_NETWORK" ] && [ "$SDA_NETWORK" != "default" ]; then
    echo "   Using SDA network: $SDA_NETWORK"
    docker run -d \
        --name sda-admin-panel \
        --network "$SDA_NETWORK" \
        -p 8001:8001 \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_PASSWORD=postgres \
        -e POSTGRES_SERVER=sda_db_1 \
        -e POSTGRES_PORT=5432 \
        -e POSTGRES_DB=sda_db \
        -e DEBUG=True \
        -e SECRET_KEY=django-insecure-change-this-in-production \
        -e ALLOWED_HOSTS="*" \
        -v sda_admin_static:/app/staticfiles \
        -v sda_admin_media:/app/media \
        --restart unless-stopped \
        sda-admin-panel
else
    echo "   Error: Could not find SDA database network"
    exit 1
fi

# Wait and check
echo "5. Waiting for admin panel to start..."
sleep 15

echo "6. Checking admin panel status..."
if docker ps | grep -q sda-admin-panel; then
    echo "   ✅ Admin panel is running successfully!"
    
    # Show recent logs
    echo ""
    echo "Recent logs:"
    docker logs sda-admin-panel --tail=15
    
    echo ""
    echo "=== Clean Deployment Complete ==="
    echo "Admin panel URL: http://your-server-ip:8001/admin/"
    echo "Username: admin"
    echo "Password: admin123"
    echo ""
    echo "IMPORTANT: Change the admin password after first login!"
else
    echo "   ❌ Admin panel failed to start"
    echo "Checking full logs..."
    docker logs sda-admin-panel
    exit 1
fi
