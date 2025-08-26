# Docker Deployment Guide for SDA Admin Panel

This guide provides multiple Docker deployment options for the SDA Django Admin Panel.

## 🚀 Quick Start

### Option 1: Full Stack (Recommended for Development)
Includes PostgreSQL and Redis containers:

```bash
# Windows
.\start-admin.bat

# Linux/Mac
chmod +x start-admin.sh
./start-admin.sh
```

### Option 2: Standalone (Connect to Existing Database)
Connects to your existing FastAPI database:

```bash
# Windows
.\start-standalone.bat

# Linux/Mac
docker-compose -f docker-compose.standalone.yml up --build
```

### Option 3: Production with Nginx
Production-ready setup with Nginx reverse proxy:

```bash
# Windows
.\start-production.bat

# Linux/Mac
docker-compose -f docker-compose.prod.yml up --build
```

## 📋 Prerequisites

- Docker and Docker Compose installed
- At least 2GB free disk space
- Ports 8001 (and 80 for production) available

## ⚙️ Configuration

### Environment Variables

Create or edit `.env` file:

```env
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_SERVER=db                    # Use 'db' for container, or IP for external DB
POSTGRES_PORT=5432
POSTGRES_DB=sda_db

# Django Settings
DEBUG=False                           # Set to True for development
SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Static and Media Files
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
```

## 🐳 Docker Compose Files

### 1. `docker-compose.yml` - Full Development Stack
- Django Admin Panel
- PostgreSQL Database
- Redis Cache
- Development server with hot reload

**Access**: http://localhost:8001/admin/

### 2. `docker-compose.standalone.yml` - Standalone Admin
- Django Admin Panel only
- Connects to external database
- Lightweight deployment

**Access**: http://localhost:8001/admin/

### 3. `docker-compose.prod.yml` - Production Setup
- Django Admin Panel with Gunicorn
- Nginx reverse proxy
- PostgreSQL Database
- Redis Cache
- Production optimizations

**Access**: http://localhost/admin/

## 🔧 Manual Commands

### Build and Start
```bash
# Development
docker-compose up --build

# Standalone
docker-compose -f docker-compose.standalone.yml up --build

# Production
docker-compose -f docker-compose.prod.yml up --build
```

### Background Mode
```bash
docker-compose up -d --build
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f sda-admin
```

### Rebuild Containers
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## 👤 Default Admin User

A default admin user is automatically created:

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@sda.com`

⚠️ **IMPORTANT**: Change this password immediately after first login!

### Create Additional Admin Users

```bash
# Access the running container
docker-compose exec sda-admin python manage.py createsuperuser

# Or use the management command
docker-compose exec sda-admin python manage.py create_admin --username newadmin --email admin@yourcompany.com --password newpassword
```

## 📊 Database Management

### Connect to Database
```bash
# If using the built-in PostgreSQL container
docker-compose exec db psql -U postgres -d sda_db

# If using external database
docker-compose exec sda-admin python manage.py dbshell
```

### Database Backup
```bash
# Backup
docker-compose exec db pg_dump -U postgres sda_db > backup.sql

# Restore
docker-compose exec -T db psql -U postgres sda_db < backup.sql
```

## 🔒 Security Considerations

### Production Checklist
- [ ] Change default admin password
- [ ] Set strong `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use strong database passwords
- [ ] Enable HTTPS (configure SSL certificates)
- [ ] Regular security updates

### Secure Environment Variables
```bash
# Generate a secure secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🚀 Production Deployment

### With External Database
1. Set up your production database
2. Update `.env` with production credentials
3. Use `docker-compose.standalone.yml`
4. Configure reverse proxy (Nginx/Apache)

### With Docker Database
1. Use `docker-compose.prod.yml`
2. Configure SSL certificates
3. Set up domain name
4. Configure firewall rules

### Environment-Specific Configs

**Development**:
```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

**Staging**:
```env
DEBUG=False
ALLOWED_HOSTS=staging.yourdomain.com
```

**Production**:
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🔍 Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs sda-admin

# Check if ports are in use
netstat -an | findstr :8001  # Windows
lsof -i :8001               # Linux/Mac
```

**Database connection failed:**
```bash
# Check database container
docker-compose logs db

# Test database connection
docker-compose exec sda-admin python manage.py check --database default
```

**Static files not loading:**
```bash
# Rebuild container to collect static files
docker-compose build --no-cache sda-admin
```

**Permission errors:**
```bash
# Fix volume permissions (Linux/Mac)
sudo chown -R 1000:1000 ./media ./staticfiles
```

### Health Checks

```bash
# Check if admin panel is responding
curl http://localhost:8001/admin/

# Check database connectivity
docker-compose exec sda-admin python manage.py migrate --check
```

## 📱 Accessing the Admin Panel

1. Start the containers using one of the methods above
2. Wait for the "Database is ready!" message
3. Open your browser and navigate to:
   - Development: http://localhost:8001/admin/
   - Production: http://localhost/admin/
4. Login with admin credentials
5. Start managing your SDA content!

## 🔄 Updates and Maintenance

### Update Admin Panel
```bash
# Pull latest changes
git pull

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Database Migration (if needed)
```bash
docker-compose exec sda-admin python manage.py migrate
```

### Backup Data
```bash
# Create backup
docker-compose exec sda-admin python manage.py dumpdata > backup.json

# Restore backup
docker-compose exec -T sda-admin python manage.py loaddata < backup.json
```

## 📞 Support

If you encounter issues:
1. Check the logs: `docker-compose logs`
2. Verify your `.env` configuration
3. Ensure Docker has sufficient resources
4. Check firewall and port availability
5. Review the troubleshooting section above
