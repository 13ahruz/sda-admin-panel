# Quick Start Commands

## Current Status
Your admin panel is currently building. Once complete, follow these steps:

## Step 1: Check if Admin Container is Running
```powershell
docker ps | Select-String "sda_admin"
```

## Step 2: Create Superuser
```powershell
docker exec -it sda_admin_local python manage.py createsuperuser
```

Follow the prompts to create:
- Username (e.g., admin)
- Email (optional, can skip)
- Password (enter twice)

## Step 3: Access Admin Panel
Open your browser and go to:
```
http://localhost:8001/admin/
```

Log in with the credentials you just created.

## Common Commands

### Check Logs
```powershell
docker logs sda_admin_local -f
```

### Restart Container
```powershell
cd C:\Users\BSShabili\Desktop\sda\admin-panel
docker-compose -f docker-compose.local.yml restart
```

### Stop Container
```powershell
docker-compose -f docker-compose.local.yml down
```

### Start Container (if stopped)
```powershell
docker-compose -f docker-compose.local.yml up -d
```

### Run Migrations
```powershell
docker exec -it sda_admin_local python manage.py migrate
```

### Collect Static Files
```powershell
docker exec -it sda_admin_local python manage.py collectstatic --noinput
```

## Troubleshooting

### Can't Connect to Database
```powershell
# Check if backend database is running
docker ps | Select-String "sda-db"

# Test database connection
docker exec -it sda_admin_local python manage.py dbshell
```

### Container Won't Start
```powershell
# View logs for errors
docker logs sda_admin_local

# Rebuild container
docker-compose -f docker-compose.local.yml up -d --build --force-recreate
```

## What's Available in Admin

Once logged in, you can manage:
- **About** - Company info (multilingual)
- **Projects** - Project portfolio (multilingual with photos)
- **News** - News articles (multilingual with sections)
- **Team Members** - Team bios (multilingual with LinkedIn)
- **Services** - Services offered (multilingual with meta)
- **Property Sectors** - Real estate sectors (multilingual)
- **Approaches** - Company approaches (multilingual)
- **Partners** - Partner information (multilingual)
- **Work Process** - Process steps (multilingual)
- **Contact Messages** - Form submissions

Each item supports:
- ✅ English (_en)
- ✅ Azerbaijani (_az)
- ✅ Russian (_ru)
