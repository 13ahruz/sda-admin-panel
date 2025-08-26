# 🔧 Fix for 400 Bad Request Error

The 400 Bad Request error is likely due to Django's ALLOWED_HOSTS setting.

## Quick Fix:

### 1. Update your .env file:

```env
# Add your server IP and domain to ALLOWED_HOSTS
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,YOUR_SERVER_IP,*

# For example, if your server IP is 123.456.789.10:
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,123.456.789.10,*

# Or allow all hosts (less secure but works):
ALLOWED_HOSTS=*
```

### 2. Restart your containers:

```bash
# Stop containers
docker-compose -f docker-compose.simple.yml down

# Start again with updated settings
docker-compose -f docker-compose.simple.yml up -d --build
```

### 3. Check if it's working:

```bash
# Check container logs for any errors
docker-compose -f docker-compose.simple.yml logs -f sda-admin
```

## Alternative: Create a quick fix .env file

```bash
# Create a new .env with permissive settings
cat > .env << EOF
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=sda_db
DEBUG=True
SECRET_KEY=django-insecure-temporary-key-change-in-production
ALLOWED_HOSTS=*
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
EOF

# Restart containers
docker-compose -f docker-compose.simple.yml down
docker-compose -f docker-compose.simple.yml up -d --build
```

## Debug Steps:

### 1. Check what IP you're using:
```bash
# Find your server's IP
curl ifconfig.me
# or
hostname -I
```

### 2. Test different URLs:
- http://localhost:8001/admin/
- http://127.0.0.1:8001/admin/
- http://YOUR_SERVER_IP:8001/admin/

### 3. Check container logs:
```bash
docker-compose -f docker-compose.simple.yml logs sda-admin
```

## Most Common Fix:
Just set `ALLOWED_HOSTS=*` in your .env file and restart the containers.
