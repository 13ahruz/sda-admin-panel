# Quick start script for admin panel with Docker (Windows PowerShell)

Write-Host "===================================" -ForegroundColor Green
Write-Host "Starting SDA Admin Panel" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit .env file with your database credentials" -ForegroundColor Red
    Write-Host "Press any key to continue after editing .env..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

Write-Host ""
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker-compose build

Write-Host ""
Write-Host "Starting admin panel..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "Waiting for container to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "===================================" -ForegroundColor Green
Write-Host "Admin Panel Status" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
docker-compose ps

Write-Host ""
Write-Host "To create a superuser, run:" -ForegroundColor Cyan
Write-Host "  docker-compose exec admin-panel python manage.py createsuperuser" -ForegroundColor White
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Cyan
Write-Host "  docker-compose logs -f" -ForegroundColor White
Write-Host ""
Write-Host "To stop:" -ForegroundColor Cyan
Write-Host "  docker-compose down" -ForegroundColor White
Write-Host ""
Write-Host "Access admin panel at:" -ForegroundColor Cyan
Write-Host "  http://localhost:8001/admin/" -ForegroundColor Yellow
Write-Host ""
