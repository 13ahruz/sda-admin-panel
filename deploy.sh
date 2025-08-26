#!/bin/bash

# SDA Django Admin Panel Deployment Script for Hostinger
# This script sets up and deploys the Django admin panel

echo "Starting SDA Django Admin Panel Deployment..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (you'll need to run this manually with your credentials)
echo "To create a superuser, run:"
echo "python manage.py createsuperuser"

# Run Django development server (for testing)
echo "To run the development server locally:"
echo "python manage.py runserver 0.0.0.0:8001"

echo "Deployment preparation complete!"
echo ""
echo "Important notes:"
echo "1. Make sure your .env file has the correct database credentials"
echo "2. Update ALLOWED_HOSTS in .env for your domain"
echo "3. Set DEBUG=False for production"
echo "4. Configure your web server (Apache/Nginx) to serve the Django app"
echo "5. Create a superuser account to access the admin panel"
