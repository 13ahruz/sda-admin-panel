#!/bin/bash

# Setup script for SDA Admin Panel

echo "==================================="
echo "SDA Admin Panel Setup"
echo "==================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created. Please update with your configuration."
else
    echo "✓ .env file already exists"
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser prompt
echo ""
echo "==================================="
echo "Create Django superuser account"
echo "==================================="
python manage.py createsuperuser

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "To start the development server:"
echo "  python manage.py runserver 8001"
echo ""
echo "To access the admin panel:"
echo "  http://localhost:8001/admin/"
echo ""
