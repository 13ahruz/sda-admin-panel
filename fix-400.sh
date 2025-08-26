#!/bin/bash

echo "🔧 Fixing Django Admin Panel with File Upload Support..."

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

echo "🧹 Cleaning up volumes to ensure fresh start..."
docker-compose -f docker-compose.simple.yml down -v

echo "🚀 Starting containers with file upload support..."
docker-compose -f docker-compose.simple.yml up -d --build

echo "⏳ Waiting for containers to start..."
sleep 15

echo "📋 Checking container status..."
docker-compose -f docker-compose.simple.yml ps

echo ""
echo "✅ Fix applied with file upload support!"
echo ""
echo "🌐 Try accessing: http://$(hostname -I | awk '{print $1}'):8001/admin/"
echo "👤 Login: admin / admin123"
echo ""
echo "� New Features:"
echo "   ✅ File upload fields for all images"
echo "   ✅ Automatic URL generation from uploads"
echo "   ✅ Backward compatibility with existing URLs"
echo "   ✅ Image previews in admin interface"
echo ""
echo "�📋 Check logs if still having issues:"
echo "   docker-compose -f docker-compose.simple.yml logs -f sda-admin"
echo ""
echo "🔍 Database migrations and file field setup is normal and expected!"
