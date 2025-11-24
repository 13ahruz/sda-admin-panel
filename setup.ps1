# Setup script for SDA Admin Panel (Windows PowerShell)

Write-Host "===================================" -ForegroundColor Green
Write-Host "SDA Admin Panel Setup" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✓ .env file created. Please update with your configuration." -ForegroundColor Green
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run migrations
Write-Host ""
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py migrate

# Collect static files
Write-Host ""
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Create superuser prompt
Write-Host ""
Write-Host "===================================" -ForegroundColor Green
Write-Host "Create Django superuser account" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
python manage.py createsuperuser

Write-Host ""
Write-Host "===================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start the development server:" -ForegroundColor Cyan
Write-Host "  python manage.py runserver 8001" -ForegroundColor White
Write-Host ""
Write-Host "To access the admin panel:" -ForegroundColor Cyan
Write-Host "  http://localhost:8001/admin/" -ForegroundColor White
Write-Host ""
