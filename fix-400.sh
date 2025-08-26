#!/bin/bash

echo "🔧 Fixing 400 Bad Request Error..."

# Create a working .env file with permissive settings
echo "📝 Creating .env file with correct settings..."
cat > .env << EOF
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=sda_db
DEBUG=True
SECRET_KEY=django-insecure-temporary-key-change-in-production
ALLOWED_HOSTS=*
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
EOF

echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.simple.yml down

echo "🚀 Starting containers with fixed settings..."
docker-compose -f docker-compose.simple.yml up -d --build

echo ""
echo "✅ Fix applied!"
echo ""
echo "🌐 Try accessing: http://$(hostname -I | awk '{print $1}'):8001/admin/"
echo "👤 Login: admin / admin123"
echo ""
echo "📋 Check logs if still having issues:"
echo "   docker-compose -f docker-compose.simple.yml logs -f sda-admin"
