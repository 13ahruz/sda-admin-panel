#!/bin/bash
# Quick start script for admin panel with Docker

echo "==================================="
echo "Starting SDA Admin Panel"
echo "==================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your database credentials"
    echo "Press any key to continue after editing .env..."
    read -n 1
fi

echo ""
echo "Building Docker image..."
docker-compose build

echo ""
echo "Starting admin panel..."
docker-compose up -d

echo ""
echo "Waiting for container to start..."
sleep 3

echo ""
echo "==================================="
echo "Admin Panel Status"
echo "==================================="
docker-compose ps

echo ""
echo "To create a superuser, run:"
echo "  docker-compose exec admin-panel python manage.py createsuperuser"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop:"
echo "  docker-compose down"
echo ""
echo "Access admin panel at:"
echo "  http://localhost:8001/admin/"
echo ""
