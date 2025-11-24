# Quick Start Guide - SDA Admin Panel

## For Local Development (Windows)

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 14+ (with existing SDA database running)
- FastAPI backend already set up

### Quick Setup

1. **Navigate to admin-panel directory**:
```powershell
cd admin-panel
```

2. **Run the setup script**:
```powershell
.\setup.ps1
```

This will:
- Create `.env` file
- Install dependencies
- Run migrations
- Collect static files
- Prompt you to create a superuser

3. **Start the admin panel**:
```powershell
python manage.py runserver 8001
```

4. **Access the admin**:
Open browser to `http://localhost:8001/admin/`
Login with your superuser credentials

## For Docker Deployment

### Option 1: With New Database

```bash
cd admin-panel
docker-compose up -d
docker-compose exec admin-panel python manage.py createsuperuser
```

Access at `http://localhost:8001/admin/`

### Option 2: Connect to Existing Backend Database

1. **Update .env** to point to your existing database:
```env
POSTGRES_SERVER=your-db-host
POSTGRES_PORT=5432
POSTGRES_DB=sda_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
```

2. **Run with standalone config**:
```bash
docker-compose -f docker-compose.standalone.yml up -d
docker-compose -f docker-compose.standalone.yml exec admin-panel python manage.py createsuperuser
```

## Common Tasks

### Create Superuser
```bash
python manage.py createsuperuser
```

### Update Database Structure (if backend changes)
```bash
python manage.py migrate
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### View Running Processes
```bash
# Docker
docker-compose ps

# Local
# Check if port 8001 is in use
netstat -ano | findstr :8001
```

## Troubleshooting

### Can't connect to database
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists: `psql -U postgres -d sda_db`

### Port 8001 already in use
Change port in command:
```bash
python manage.py runserver 8002
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Permission denied on setup.ps1
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```

## Next Steps

After successful setup:
1. Login to admin panel
2. Navigate through different models
3. Test creating/editing content
4. Verify changes appear in FastAPI backend
5. Check that multilingual fields work correctly

## Security Notes

- Change `DJANGO_SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use strong passwords for superuser
- Consider IP whitelisting for admin access
- Enable HTTPS in production

## Support

For issues:
1. Check logs: `docker-compose logs -f` or console output
2. Verify database connection
3. Ensure backend database is accessible
4. Check Django version compatibility
