# Simple Server Deployment Commands

## For Production Server Deployment:

```bash
# 1. Clone/upload your admin-panel folder to server
# 2. Navigate to admin-panel directory
cd admin-panel

# 3. Create environment file (copy from your FastAPI backend or edit manually)
cp .env.example .env
# Edit .env with your production database credentials

# 4. Build and start in background (detached mode)
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# That's it! Your admin panel is running in background
```

## Alternative - One Line Command:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## To Check Status:
```bash
# Check if containers are running
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

## Access Your Admin Panel:
- **URL**: http://your-server-ip/admin/
- **Username**: admin
- **Password**: admin123 (change immediately!)

## Important Notes:
- Make sure ports 80 and 5432 are available on your server
- Update your .env file with correct database credentials
- The admin panel will be available at port 80 (http://your-server-ip/admin/)
- Change the default admin password after first login
