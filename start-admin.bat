@echo off
echo Starting SDA Admin Panel with Docker Compose...
echo.

echo Checking if .env file exists...
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file with your database credentials!
    echo.
    pause
)

echo Building and starting containers...
docker-compose up --build

echo.
echo Admin Panel should be available at: http://localhost:8001/admin/
echo Default credentials: admin / admin123
echo IMPORTANT: Change the password after first login!
echo.
pause
