@echo off
echo Starting SDA Django Admin Panel Setup...

echo Installing Python dependencies...
pip install -r requirements.txt

echo Collecting static files...
python manage.py collectstatic --noinput

echo Setup complete!
echo.
echo Next steps:
echo 1. Update your .env file with the correct database credentials
echo 2. Create a superuser: python manage.py createsuperuser
echo 3. Run the server: python manage.py runserver 0.0.0.0:8001
echo 4. Access admin at: http://localhost:8001/admin/
echo.
pause
