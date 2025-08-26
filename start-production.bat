@echo off
echo Starting SDA Admin Panel (Production with Nginx)...
echo.

echo Checking if .env file exists...
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file with your production settings!
    echo Set DEBUG=False and update SECRET_KEY and ALLOWED_HOSTS!
    echo.
    pause
)

echo Building and starting production containers...
docker-compose -f docker-compose.prod.yml up --build

echo.
echo Admin Panel should be available at: http://localhost/admin/
echo Default credentials: admin / admin123
echo IMPORTANT: Change the password after first login!
echo.
pause
