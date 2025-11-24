# Production Deployment Guide

## Pre-Deployment Checklist

### 1. Environment Configuration

Update `.env` file with production values:

```env
# Database Configuration
POSTGRES_DB=sda_db
POSTGRES_USER=sda_admin
POSTGRES_PASSWORD=<strong-password>
POSTGRES_SERVER=<your-db-host>
POSTGRES_PORT=5432

# Django Configuration
DJANGO_SECRET_KEY=<generate-strong-random-key>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,153.92.223.91

# Media Files
MEDIA_ROOT=/var/www/sda/uploads
```

### 2. Generate Secret Key

```python
# Run in Python shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 3. Security Settings

- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use strong database password
- [ ] Use strong Django secret key
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall (allow only 8001 from trusted IPs)

## Deployment Options

### Option 1: Docker Deployment (Recommended)

#### Step 1: Prepare Server

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Step 2: Transfer Files

```bash
# From local machine
scp -r admin-panel user@153.92.223.91:/var/www/sda/
```

#### Step 3: Configure Environment

```bash
cd /var/www/sda/admin-panel
cp .env.example .env
nano .env  # Update with production values
```

#### Step 4: Build and Run

```bash
# If connecting to existing database (recommended)
docker-compose -f docker-compose.standalone.yml up -d

# Or with new database
docker-compose up -d
```

#### Step 5: Create Superuser

```bash
docker-compose exec admin-panel python manage.py createsuperuser
```

#### Step 6: Collect Static Files

```bash
docker-compose exec admin-panel python manage.py collectstatic --noinput
```

### Option 2: Manual Deployment with Gunicorn

#### Step 1: Install System Dependencies

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip postgresql-client nginx
```

#### Step 2: Setup Virtual Environment

```bash
cd /var/www/sda/admin-panel
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### Step 3: Configure Environment

```bash
cp .env.example .env
nano .env  # Update with production values
```

#### Step 4: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

#### Step 6: Create Systemd Service

Create `/etc/systemd/system/sda-admin.service`:

```ini
[Unit]
Description=SDA Admin Panel
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/sda/admin-panel
Environment="PATH=/var/www/sda/admin-panel/venv/bin"
ExecStart=/var/www/sda/admin-panel/venv/bin/gunicorn \
    --workers 3 \
    --bind 0.0.0.0:8001 \
    --timeout 120 \
    --access-logfile /var/log/sda-admin/access.log \
    --error-logfile /var/log/sda-admin/error.log \
    admin_panel.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### Step 7: Create Log Directory

```bash
sudo mkdir -p /var/log/sda-admin
sudo chown www-data:www-data /var/log/sda-admin
```

#### Step 8: Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable sda-admin
sudo systemctl start sda-admin
sudo systemctl status sda-admin
```

### Option 3: Nginx Reverse Proxy (Optional)

Create `/etc/nginx/sites-available/sda-admin`:

```nginx
server {
    listen 80;
    server_name admin.sdaconsulting.az;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name admin.sdaconsulting.az;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/sda-admin.crt;
    ssl_certificate_key /etc/ssl/private/sda-admin.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static Files
    location /static/ {
        alias /var/www/sda/admin-panel/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media Files
    location /media/ {
        alias /var/www/sda/uploads/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Admin Panel
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # IP Whitelisting (Optional)
    # allow 192.168.1.0/24;  # Office network
    # deny all;

    client_max_body_size 50M;
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/sda-admin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## SSL/TLS Configuration

### Using Let's Encrypt (Free SSL)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d admin.sdaconsulting.az

# Auto-renewal (already configured by certbot)
sudo certbot renew --dry-run
```

## Monitoring & Maintenance

### View Logs

```bash
# Docker
docker-compose logs -f admin-panel

# Systemd
sudo journalctl -u sda-admin -f

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Restart Services

```bash
# Docker
docker-compose restart admin-panel

# Systemd
sudo systemctl restart sda-admin

# Nginx
sudo systemctl reload nginx
```

### Database Backup

```bash
# Create backup
pg_dump -U sda_admin -h localhost sda_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
psql -U sda_admin -h localhost sda_db < backup_20231124_120000.sql
```

### Update Deployment

```bash
# Pull latest changes
cd /var/www/sda/admin-panel
git pull  # if using git

# Docker deployment
docker-compose down
docker-compose build
docker-compose up -d

# Manual deployment
source venv/bin/activate
pip install -r requirements.txt --upgrade
python manage.py collectstatic --noinput
sudo systemctl restart sda-admin
```

## Performance Optimization

### 1. Database Connection Pooling

Update settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_SERVER'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

### 2. Static File Caching

Nginx already configured with 30-day cache for static files.

### 3. Gunicorn Workers

Calculate workers: `(2 * CPU_CORES) + 1`

For 2 CPU cores: `--workers 5`

### 4. Enable Gzip Compression

In nginx config:

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/json application/javascript;
```

## Firewall Configuration

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow admin panel (if direct access needed)
sudo ufw allow 8001/tcp

# Enable firewall
sudo ufw enable
```

## Health Checks

Create `/var/www/sda/admin-panel/healthcheck.sh`:

```bash
#!/bin/bash

# Check if admin panel is responding
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/admin/login/)

if [ $response -eq 200 ]; then
    echo "✓ Admin panel is healthy"
    exit 0
else
    echo "✗ Admin panel is down (HTTP $response)"
    exit 1
fi
```

Make executable:

```bash
chmod +x /var/www/sda/admin-panel/healthcheck.sh
```

Add to crontab for monitoring:

```bash
# Check every 5 minutes
*/5 * * * * /var/www/sda/admin-panel/healthcheck.sh >> /var/log/sda-admin-health.log 2>&1
```

## Troubleshooting Production Issues

### Issue: 502 Bad Gateway

```bash
# Check if gunicorn is running
sudo systemctl status sda-admin

# Check logs
sudo journalctl -u sda-admin -n 50

# Restart service
sudo systemctl restart sda-admin
```

### Issue: Static files not loading

```bash
# Recollect static files
cd /var/www/sda/admin-panel
source venv/bin/activate
python manage.py collectstatic --noinput

# Check nginx config
sudo nginx -t
```

### Issue: Database connection errors

```bash
# Test database connection
psql -U sda_admin -h localhost -d sda_db

# Check PostgreSQL status
sudo systemctl status postgresql

# View PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

## Security Hardening

### 1. Disable Root Login

```bash
# Edit SSH config
sudo nano /etc/ssh/sshd_config

# Set: PermitRootLogin no
sudo systemctl restart sshd
```

### 2. Setup Fail2Ban

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Regular Updates

```bash
sudo apt update
sudo apt upgrade -y
```

### 4. Database Security

```sql
-- Restrict database user permissions
REVOKE ALL ON DATABASE sda_db FROM PUBLIC;
GRANT CONNECT ON DATABASE sda_db TO sda_admin;
GRANT ALL ON ALL TABLES IN SCHEMA public TO sda_admin;
```

## Rollback Plan

If deployment fails:

1. **Docker**: 
```bash
docker-compose down
docker-compose up -d --force-recreate
```

2. **Manual**:
```bash
# Restore from backup
psql -U sda_admin sda_db < backup.sql

# Restart service
sudo systemctl restart sda-admin
```

## Post-Deployment Verification

- [ ] Admin login works
- [ ] All models visible
- [ ] Can create/edit records
- [ ] Images display correctly
- [ ] Static files load
- [ ] HTTPS works
- [ ] Logs are clean
- [ ] Performance is acceptable

## Support Contacts

- **System Admin**: [Your contact]
- **Database**: [Your contact]
- **Security**: [Your contact]

## Conclusion

Your admin panel is now deployed and ready for production use. Monitor logs regularly and perform routine maintenance to ensure optimal performance.
