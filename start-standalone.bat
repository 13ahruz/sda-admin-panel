@echo off
echo Starting SDA Admin Panel (Standalone - connects to existing database)...
echo.

echo This will connect to your existing FastAPI database.
echo Make sure your FastAPI backend database is running.
echo.

echo Checking if .env file exists...
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file with your database credentials!
    echo Update POSTGRES_SERVER to point to your existing database.
    echo.
    pause
)

echo Building and starting admin panel...
docker-compose -f docker-compose.standalone.yml up --build

echo.
echo Admin Panel should be available at: http://localhost:8001/admin/
echo Default credentials: admin / admin123
echo IMPORTANT: Change the password after first login!
echo.
pause
