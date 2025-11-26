#!/bin/bash

# Fix nginx upload limit for admin panel
echo "Fixing nginx configuration for admin panel file uploads..."

# Backup current config
sudo cp /etc/nginx/sites-available/sdaconsulting.az /etc/nginx/sites-available/sdaconsulting.az.backup-$(date +%s)

# Add client_max_body_size to admin location block
sudo sed -i '/location \/admin\/ {/a\        client_max_body_size 50M;' /etc/nginx/sites-available/sdaconsulting.az

# Test nginx configuration
echo "Testing nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "Configuration is valid. Reloading nginx..."
    sudo systemctl reload nginx
    echo "✅ Nginx configuration updated successfully!"
    echo "File upload limit for /admin/ is now 50MB"
else
    echo "❌ Nginx configuration test failed. Restoring backup..."
    sudo cp /etc/nginx/sites-available/sdaconsulting.az.backup-$(date +%s) /etc/nginx/sites-available/sdaconsulting.az
    exit 1
fi
