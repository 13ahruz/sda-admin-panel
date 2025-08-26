# 🔧 Quick Fix for Port 80 Conflict

Port 80 is already in use on your server. Here are your options:

## Option 1: Use Simple Setup (Recommended)
This skips Nginx and runs Django directly on port 8001:

```bash
# Stop any running containers first
docker-compose -f docker-compose.prod.yml down

# Use the simple setup
docker-compose -f docker-compose.simple.yml up -d --build
```

**Access**: http://your-server-ip:8001/admin/

## Option 2: Use Alternative Ports
This uses Nginx on port 8080 instead of 80:

```bash
# Stop any running containers first
docker-compose -f docker-compose.prod.yml down

# Use alternative port setup
docker-compose -f docker-compose.prod-alt.yml up -d --build
```

**Access**: http://your-server-ip:8080/admin/

## Option 3: Stop Service Using Port 80
Find and stop whatever is using port 80:

```bash
# Find what's using port 80
sudo netstat -tulpn | grep :80
# or
sudo lsof -i :80

# Stop the service (example for Apache)
sudo systemctl stop apache2
# or for Nginx
sudo systemctl stop nginx

# Then use original production setup
docker-compose -f docker-compose.prod.yml up -d --build
```

## Option 4: Use Different External Port
Modify your existing docker-compose.prod.yml:

Change this line:
```yaml
ports:
  - "80:80"  # This causes the conflict
```

To:
```yaml
ports:
  - "8080:80"  # Use port 8080 instead
```

## Recommended Quick Solution:

```bash
# Clean up first
docker-compose -f docker-compose.prod.yml down

# Use simple setup (no Nginx, direct Django access)
docker-compose -f docker-compose.simple.yml up -d --build

# Check if running
docker-compose -f docker-compose.simple.yml ps
```

**Your admin panel will be available at**: http://your-server-ip:8001/admin/
