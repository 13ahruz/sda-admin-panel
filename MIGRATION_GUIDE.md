# Quick Migration Guide

## Step-by-Step: Applying Admin Panel Updates

### Step 1: Backup Current Data (IMPORTANT!)
```bash
# Backup your database
docker exec sda_postgres pg_dump -U postgres sda_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Step 2: Stop Running Containers
```bash
# Stop admin panel if running
cd admin-panel
docker-compose down

# Stop backend if needed
cd ../sda
docker-compose down
```

### Step 3: Apply Database Migrations

The models have been updated but the database might already have the correct schema (since backend was using it). Let's check and apply migrations:

```bash
cd admin-panel

# For local development
docker-compose -f docker-compose.local.yml up -d

# Check for migrations
docker exec -it sda_admin_local python manage.py showmigrations

# Create new migrations if needed
docker exec -it sda_admin_local python manage.py makemigrations

# Apply migrations
docker exec -it sda_admin_local python manage.py migrate

# Stop container
docker-compose -f docker-compose.local.yml down
```

### Step 4: Start Backend First
```bash
cd ../sda

# For local development
docker-compose -f docker-compose.local.yml up -d

# Wait for backend to be healthy
docker-compose -f docker-compose.local.yml logs -f backend

# For Hostinger
docker-compose -f docker-compose.hostinger.yml up -d
```

### Step 5: Start Admin Panel
```bash
cd ../admin-panel

# For local development
cp .env.local .env
docker-compose -f docker-compose.local.yml up -d

# For Hostinger
cp .env.hostinger .env
# IMPORTANT: Edit .env and update passwords!
nano .env  # or your preferred editor
docker-compose -f docker-compose.hostinger.yml up -d
```

### Step 6: Create Superuser (First Time Only)
```bash
# Local
docker exec -it sda_admin_local python manage.py createsuperuser

# Hostinger
docker exec -it sda_admin_hostinger python manage.py createsuperuser
```

### Step 7: Collect Static Files (Production)
```bash
# Only for Hostinger/Production
docker exec -it sda_admin_hostinger python manage.py collectstatic --noinput
```

### Step 8: Verify Everything Works

1. **Access Admin Panel:**
   - Local: http://localhost:8001/admin/
   - Hostinger: https://sdaconsulting.az:8001/admin/

2. **Test Each Model:**
   - Projects - Check multilingual title/description fields
   - News - Check multilingual title/summary fields
   - Team Members - Check multilingual name/role/bio + linkedin_url
   - Services - Check multilingual fields + slug
   - All others - Verify multilingual fields appear

3. **Test File Upload:**
   - Try uploading an image in Projects
   - Verify image appears and URL is saved

4. **Check Backend Integration:**
   - Access backend API: http://localhost:8000/docs (or https://sdaconsulting.az/docs)
   - Verify data entered in admin appears in API responses

---

## Troubleshooting Common Issues

### Issue: Migrations conflict
**Solution:**
```bash
# Fake initial migration if tables already exist
docker exec -it sda_admin_local python manage.py migrate --fake-initial

# Or reset migrations (careful!)
docker exec -it sda_admin_local python manage.py migrate sda_models zero
docker exec -it sda_admin_local python manage.py migrate
```

### Issue: Admin panel can't connect to database
**Solution:**
```bash
# Check backend network exists
docker network ls | grep sda_network

# Recreate network if needed
docker network create sda_network

# Verify backend database is running
docker ps | grep postgres

# Check connection
docker exec -it sda_admin_local python manage.py dbshell
```

### Issue: File uploads don't work
**Solution:**
1. Check `BACKEND_UPLOAD_URL` in `.env`
2. Verify backend is accessible:
   ```bash
   # From admin container
   docker exec -it sda_admin_local curl http://backend:8000/docs
   ```
3. Check backend logs:
   ```bash
   docker logs sda_backend
   ```

### Issue: Multilingual fields not showing
**Solution:**
1. Clear browser cache
2. Restart admin container:
   ```bash
   docker-compose restart
   ```
3. Check migrations were applied:
   ```bash
   docker exec -it sda_admin_local python manage.py showmigrations
   ```

### Issue: Some models missing in admin
**Solution:**
```bash
# Check admin.py registrations
docker exec -it sda_admin_local python manage.py shell
>>> from django.contrib import admin
>>> admin.site._registry.keys()
```

---

## Rolling Back (If Needed)

If something goes wrong:

1. **Restore database from backup:**
   ```bash
   docker exec -i sda_postgres psql -U postgres sda_db < backup_YYYYMMDD_HHMMSS.sql
   ```

2. **Revert code changes:**
   ```bash
   git checkout HEAD -- admin-panel/sda_models/models.py
   git checkout HEAD -- admin-panel/sda_models/admin.py
   ```

3. **Restart containers:**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

---

## Post-Migration Checklist

- [ ] Database backup created
- [ ] Backend running and accessible
- [ ] Admin panel running and accessible
- [ ] Can log in to admin panel
- [ ] All models visible in admin
- [ ] Multilingual fields appear correctly
- [ ] Can create/edit/delete records
- [ ] File uploads work
- [ ] Data visible in backend API
- [ ] No error logs in containers

---

## Quick Commands Reference

```bash
# View logs
docker-compose logs -f

# Restart containers
docker-compose restart

# Enter container shell
docker exec -it sda_admin_local bash

# Django shell
docker exec -it sda_admin_local python manage.py shell

# Database shell
docker exec -it sda_admin_local python manage.py dbshell

# Create superuser
docker exec -it sda_admin_local python manage.py createsuperuser

# Check migrations
docker exec -it sda_admin_local python manage.py showmigrations

# Make migrations
docker exec -it sda_admin_local python manage.py makemigrations

# Apply migrations
docker exec -it sda_admin_local python manage.py migrate

# Collect static files
docker exec -it sda_admin_local python manage.py collectstatic --noinput
```

---

**Ready to migrate!** Start with Step 1 and follow through each step carefully.
