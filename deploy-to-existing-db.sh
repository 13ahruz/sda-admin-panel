#!/bin/bash

echo "=== SDA Admin Panel - Connect to Existing Database ==="
echo "This script deploys the admin panel to connect to your existing SDA database"
echo ""

# Stop any existing admin panel containers
echo "1. Stopping existing admin panel containers..."
docker-compose -f docker-compose.simple.yml down 2>/dev/null || true
docker-compose -f docker-compose.existing-db.yml down 2>/dev/null || true
docker stop sda-admin-panel 2>/dev/null || true
docker rm sda-admin-panel 2>/dev/null || true

# Build the updated admin panel
echo "2. Building updated admin panel with corrected models..."
docker build -t sda-admin-panel .

# Start with connection to existing database
echo "3. Starting admin panel connected to existing SDA database..."

# Check if main SDA backend is running and get its network
SDA_NETWORK=$(docker inspect sda_db_1 2>/dev/null | grep -o '"NetworkMode": "[^"]*"' | cut -d'"' -f4)
if [ ! -z "$SDA_NETWORK" ] && [ "$SDA_NETWORK" != "default" ]; then
    echo "   Using SDA network: $SDA_NETWORK"
    # Run with existing network
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
    echo "   Using docker-compose with external database connection..."
    # Use docker-compose with external database
    cat > docker-compose.temp.yml << EOF
version: '3.8'

services:
  sda-admin:
    image: sda-admin-panel
    container_name: sda-admin-panel
    ports:
      - "8001:8001"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_SERVER=host.docker.internal
      - POSTGRES_PORT=5432
      - POSTGRES_DB=sda_db
      - DEBUG=True
      - SECRET_KEY=django-insecure-change-this-in-production
      - ALLOWED_HOSTS=*
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    restart: unless-stopped
    extra_hosts:
      - "host.docker.internal:host-gateway"

volumes:
  static_volume:
  media_volume:
EOF

    docker-compose -f docker-compose.temp.yml up -d
fi

# Wait for container to start
echo "4. Waiting for admin panel to start..."
sleep 10

# Check if it's working
echo "5. Checking admin panel status..."
if docker ps | grep -q sda-admin-panel; then
    echo "   ✅ Admin panel is running"
    docker logs sda-admin-panel --tail=10
    echo ""
    echo "=== Deployment Complete ==="
    echo "Admin panel URL: http://your-server-ip:8001/admin/"
    echo "Username: admin"
    echo "Password: admin123"
    echo ""
    echo "IMPORTANT: Change the admin password after first login!"
else
    echo "   ❌ Admin panel failed to start"
    echo "Checking logs..."
    docker logs sda-admin-panel
fi

# Cleanup temp file
rm -f docker-compose.temp.yml

echo "To check logs: docker logs sda-admin-panel"
echo "To restart: docker restart sda-admin-panel"
