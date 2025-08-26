@echo off
echo 🚀 Deploying SDA Admin Panel on Server...

REM Check if .env exists
if not exist .env (
    echo 📋 Creating .env from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file with your production database credentials!
    echo ⚠️  Update POSTGRES_SERVER, POSTGRES_PASSWORD, SECRET_KEY, and ALLOWED_HOSTS
    echo.
    echo Press Enter after updating .env file...
    pause
)

echo 🔨 Building and starting containers in background...
docker-compose -f docker-compose.prod.yml up -d --build

echo.
echo ✅ Deployment Complete!
echo.
echo 🌐 Admin Panel URL: http://localhost/admin/
echo 👤 Default Login: admin / admin123
echo ⚠️  IMPORTANT: Change the default password immediately!
echo.
echo 📊 To check status: docker-compose -f docker-compose.prod.yml ps
echo 📋 To view logs: docker-compose -f docker-compose.prod.yml logs -f
echo 🛑 To stop: docker-compose -f docker-compose.prod.yml down
echo.
pause
