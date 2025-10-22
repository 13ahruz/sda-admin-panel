# SDA Admin Panel - Updated Structure

## Overview
The admin panel has been updated to match the backend's multilingual data structure. All models now support English (_en), Azerbaijani (_az), and Russian (_ru) fields.

## What Changed

### 1. Models Updated
All models in `sda_models/models.py` now include:
- Multilingual fields with `_en`, `_az`, `_ru` suffixes
- Legacy fields kept for backward compatibility
- Proper field naming matching the FastAPI backend

**Updated Models:**
- `About` - experience, project_count, members (all multilingual)
- `PropertySector` - title, description (multilingual)
- `Project` - title, description (multilingual) + slug field added
- `News` & `NewsSection` - title, summary, heading, content (multilingual)
- `TeamMember` - full_name, role, bio (multilingual) + linkedin_url added
- `Service` - name, description, hero_text, meta_title, meta_description (multilingual) + slug, image_url added
- `Approach` - title, description (multilingual)
- `Partner` - title, button_text (multilingual)
- `WorkProcess` - title, description (multilingual)
- `ContactMessage` - no changes (no multilingual needed)

### 2. Admin Interface Enhanced
The admin interface (`sda_models/admin.py`) now:
- Shows multilingual fields in organized fieldsets (English, Azerbaijani, Russian)
- Legacy fields are collapsed by default
- List displays show English fields primarily
- Search works across all language variants
- File upload integration with backend API maintained

### 3. Database Configuration
- Admin panel now correctly connects to the **same database** as the backend
- Uses external network `sda_network` from backend's docker-compose
- Database host is `db` (same as backend)

### 4. Docker Compose Files
**Kept only 2 files:**
- `docker-compose.local.yml` - For local development
- `docker-compose.hostinger.yml` - For Hostinger VPS production

**Removed:**
- docker-compose.yml
- docker-compose.standalone.yml
- docker-compose.simple.yml
- docker-compose.prod.yml
- docker-compose.prod-alt.yml
- docker-compose.fixed.yml

### 5. Environment Files
- `.env` - Default configuration
- `.env.local` - Local development settings
- `.env.hostinger` - Hostinger production settings

## How to Use

### Local Development

1. **Start the backend first:**
   ```bash
   cd ../sda
   docker-compose -f docker-compose.local.yml up -d
   ```

2. **Start admin panel:**
   ```bash
   cd ../admin-panel
   cp .env.local .env
   docker-compose -f docker-compose.local.yml up -d
   ```

3. **Access admin panel:**
   - URL: http://localhost:8001/admin/
   - Backend API: http://localhost:8000

4. **Create superuser (first time only):**
   ```bash
   docker exec -it sda_admin_local python manage.py createsuperuser
   ```

### Hostinger Production

1. **Ensure backend is running:**
   ```bash
   cd ../sda
   docker-compose -f docker-compose.hostinger.yml up -d
   ```

2. **Deploy admin panel:**
   ```bash
   cd ../admin-panel
   cp .env.hostinger .env
   # Update passwords in .env
   docker-compose -f docker-compose.hostinger.yml up -d
   ```

3. **Access admin panel:**
   - URL: https://sdaconsulting.az:8001/admin/
   - Backend API: https://sdaconsulting.az

## Important Notes

### Database Schema
The admin panel uses the **exact same database tables** as the FastAPI backend. No separate database needed.

### Migrations
When you update models:
```bash
docker exec -it sda_admin_local python manage.py makemigrations
docker exec -it sda_admin_local python manage.py migrate
```

### File Uploads
File uploads are handled by the backend API. The admin panel sends files to:
- Local: `http://localhost:8000/api/v1/upload`
- Production: `https://sdaconsulting.az/api/v1/upload`

### Network Configuration
- **Local**: Admin panel and backend share `sda_network` bridge network
- **Hostinger**: Admin panel connects to backend's external `sda_network`

## Multilingual Data Entry

When adding/editing content:

1. **English fields** - Primary language, shown first
2. **Azerbaijani fields** - Collapsed section, expand to edit
3. **Russian fields** - Collapsed section, expand to edit
4. **Legacy fields** - Old single-language fields, kept for compatibility

**Best Practice:** Always fill at least the English fields. Other languages are optional but recommended.

## Troubleshooting

### Admin can't connect to database
- Ensure backend is running first
- Check that backend's `sda_network` exists: `docker network ls`
- Verify database credentials in `.env`

### File uploads not working
- Check `BACKEND_UPLOAD_URL` in `.env`
- Ensure backend API is accessible
- Verify backend's upload endpoint is working

### Models not showing in admin
- Run migrations: `python manage.py migrate`
- Check that models are registered in `admin.py`

### Changes not reflecting
- Clear browser cache
- Restart admin container: `docker-compose restart`
- Collect static files: `python manage.py collectstatic --noinput`

## Structure Summary

```
admin-panel/
├── docker-compose.local.yml      # Local development
├── docker-compose.hostinger.yml  # Production deployment
├── .env                          # Current environment config
├── .env.local                    # Local settings
├── .env.hostinger                # Production settings
├── Dockerfile                    # Container build
├── requirements.txt              # Python dependencies
├── manage.py                     # Django management
├── sda_admin/                    # Django project settings
│   ├── settings.py               # Updated with DB config
│   ├── urls.py
│   └── wsgi.py
└── sda_models/                   # Django app
    ├── models.py                 # ✅ Updated with multilingual
    ├── admin.py                  # ✅ Updated with multilingual
    ├── forms.py
    └── migrations/
```

## Backend Connection

The admin panel connects to backend's PostgreSQL database:
- **Host:** `db` (Docker service name)
- **Port:** `5432`
- **Database:** `sda_db`
- **User:** `postgres`
- **Tables:** Shared with FastAPI backend

No data duplication - single source of truth!
