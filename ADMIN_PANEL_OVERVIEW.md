# SDA Admin Panel - Complete Overview

## What Has Been Created

A complete Django admin panel that manages your FastAPI backend's PostgreSQL database. The admin panel provides a professional, user-friendly interface to manage all your website content.

## Project Structure

```
admin-panel/
├── admin_panel/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py             # Main configuration
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI config
│   └── asgi.py                 # ASGI config
│
├── sda_backend/                # Main Django app
│   ├── __init__.py
│   ├── apps.py                 # App configuration
│   ├── models.py               # Database models (mirrors FastAPI)
│   ├── admin.py                # Admin interface configuration
│   └── migrations/             # Database migrations
│       └── __init__.py
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Full stack deployment
├── docker-compose.standalone.yml # Connect to existing DB
├── setup.sh                    # Linux/Mac setup script
├── setup.ps1                   # Windows PowerShell setup script
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # Comprehensive documentation
└── QUICKSTART.md              # Quick start guide
```

## Features Implemented

### 1. All Backend Models Mapped
✅ **Projects** - With photos, sectors, multilingual content
✅ **News** - With sections and multilingual support
✅ **Services** - With benefits and SEO metadata
✅ **Team Members** - With LinkedIn integration
✅ **Property Sectors** - With inns (features)
✅ **Work Processes** - Company work methodology
✅ **Approaches** - Company approaches
✅ **About** - Company information with logos
✅ **Partners** - Partner logos and info
✅ **Contact Messages** - With status tracking

### 2. Multilingual Support
Each model with multilingual fields shows organized fieldsets:
- **English (EN)** - Primary language
- **Azərbaycan (AZ)** - Azerbaijani
- **Русский (RU)** - Russian
- **Legacy** - Collapsed by default for backward compatibility

### 3. Advanced Admin Features

#### Inline Editing
- **Project Photos** - Add/edit multiple photos within project
- **News Sections** - Add/edit sections within news article
- **Sector Inns** - Add/edit features within property sector
- **Team Section Items** - Add/edit items within team section
- **About Logos** - Add/edit logos within about section
- **Partner Logos** - Add/edit logos within partner

#### Image Previews
- Project photos and covers
- News photos
- Team member photos
- Service icons
- Work process images
- Logo previews for About and Partners

#### Advanced Filtering
- Filter by property sector, year, tags
- Filter by creation date
- Filter contact messages by status, read/unread
- Filter by property type

#### Search Capabilities
- Search across all multilingual fields
- Search by email, phone, name in contacts
- Search by slug, client name in projects
- Full-text search support

#### Bulk Actions
- Mark contact messages as read/unread
- Update contact message status (new/in progress/resolved)
- Batch operations on multiple records

#### Smart Displays
- Show related counts (photos, sections, logos)
- Display primary language with fallback
- Color-coded message types (Career/Contact)
- Sortable columns with drag-and-drop ordering

### 4. Database Configuration

The admin panel uses **`managed=False`** for all models, which means:
- ✅ Django reads from existing database
- ✅ Django can update existing records
- ✅ No schema conflicts with FastAPI
- ✅ FastAPI remains source of truth
- ✅ Safe to use alongside backend

### 5. Security Features

- Environment-based configuration
- Secret key management
- ALLOWED_HOSTS restriction
- Debug mode control
- User authentication required
- Superuser permission system

## How It Works

### Database Connection
```
FastAPI Backend (Port 8000) ─┐
                             ├─→ PostgreSQL Database (Port 5432)
Django Admin (Port 8001) ────┘
```

Both applications connect to the same database:
- FastAPI handles API requests and frontend
- Django Admin provides management interface
- No data duplication or synchronization needed

### File Uploads

The admin displays images from the FastAPI uploads folder:
```
sda/uploads/          ← FastAPI saves here
    ├── projects/
    ├── team/
    ├── services/
    └── ...

admin-panel/          ← Django reads from above
    └── settings.py (MEDIA_ROOT points to uploads)
```

### Workflow

1. **FastAPI Backend** - Serves API and handles uploads
2. **Django Admin** - Manages database content
3. **Frontend** - Fetches data via FastAPI API
4. **Database** - Single source of truth

## Getting Started

### Method 1: Local Development (Recommended for testing)

```powershell
cd admin-panel
.\setup.ps1
python manage.py runserver 8001
```

Access: http://localhost:8001/admin/

### Method 2: Docker (Recommended for production)

```bash
cd admin-panel
docker-compose up -d
docker-compose exec admin-panel python manage.py createsuperuser
```

Access: http://localhost:8001/admin/

## Configuration

### Environment Variables (.env)

```env
# Database (same as FastAPI)
POSTGRES_DB=sda_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432

# Django
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Media
MEDIA_ROOT=../sda/uploads
```

## Common Use Cases

### Adding a New Project
1. Login to admin
2. Click "Projects" → "Add Project"
3. Fill multilingual fields (title, description)
4. Set slug, client, year, sector
5. Add cover photo URL
6. Add multiple photos with inline form
7. Save

### Managing Contact Messages
1. Navigate to "Contact Messages"
2. Filter by status or type
3. Click message to view details
4. Update status and mark as read
5. Take appropriate action

### Updating Team Member
1. Go to "Team Members"
2. Find and click member
3. Update name, role, bio (all languages)
4. Update photo URL or LinkedIn
5. Save changes

### Reordering Items
1. Navigate to model with order field
2. Click inline edit on list view
3. Change order numbers
4. Save to update display sequence

## Management Commands

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver 8001

# Run on different port
python manage.py runserver 8002

# Create database backup
python manage.py dumpdata > backup.json

# Load data
python manage.py loaddata backup.json
```

## Production Deployment

### Security Checklist
- [ ] Set strong `DJANGO_SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use HTTPS/SSL
- [ ] Set strong superuser password
- [ ] Enable IP whitelisting if needed
- [ ] Configure proper firewall rules
- [ ] Regular database backups

### Performance Tips
- Use gunicorn or uWSGI for production
- Configure nginx reverse proxy
- Enable database connection pooling
- Set up proper caching
- Monitor resource usage

## Troubleshooting

### Issue: Can't connect to database
**Solution**: 
- Check PostgreSQL is running
- Verify credentials in `.env`
- Test connection: `psql -U postgres -d sda_db`

### Issue: Images not showing
**Solution**:
- Check `MEDIA_ROOT` path in settings
- Verify uploads directory exists
- Check file permissions

### Issue: Permission denied
**Solution**:
- Ensure superuser is created
- Check database user has proper privileges
- Verify file system permissions

### Issue: Port already in use
**Solution**:
```bash
# Find process using port
netstat -ano | findstr :8001

# Kill process or use different port
python manage.py runserver 8002
```

## Advantages of This Setup

1. **No Code Duplication** - Models defined once in FastAPI
2. **Single Database** - No synchronization needed
3. **Non-Invasive** - Doesn't modify FastAPI backend
4. **Full Featured** - Complete CRUD operations
5. **User Friendly** - Django admin is intuitive
6. **Multilingual** - Proper language support
7. **Scalable** - Can handle production workload
8. **Maintainable** - Easy to update and extend

## Extending the Admin

### Add Custom Actions
Edit `sda_backend/admin.py`:
```python
@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    actions = ['custom_action']
    
    def custom_action(self, request, queryset):
        # Your logic here
        pass
    custom_action.short_description = "Description"
```

### Customize Display
```python
def custom_field_display(self, obj):
    return format_html('<span>{}</span>', obj.field)
custom_field_display.short_description = 'Label'
```

### Add Filters
```python
class YourModelAdmin(admin.ModelAdmin):
    list_filter = ('field1', 'field2', 'created_at')
```

## Support & Maintenance

### Regular Tasks
- Backup database weekly
- Review contact messages daily
- Update content as needed
- Monitor error logs
- Update dependencies quarterly

### Logs Location
- **Local**: Console output
- **Docker**: `docker-compose logs -f admin-panel`
- **Production**: Configure proper logging

## Conclusion

You now have a fully functional Django admin panel that:
- Connects to your FastAPI backend database
- Manages all content types
- Supports multilingual content
- Provides intuitive interface
- Includes comprehensive documentation
- Ready for both development and production

The admin panel is completely separate from your FastAPI backend and won't interfere with its operation. Both systems work together seamlessly to provide a complete content management solution.

## Next Steps

1. Run setup script to initialize
2. Create superuser account
3. Login and explore the admin
4. Test creating/editing content
5. Verify changes in frontend
6. Deploy to production when ready

**Happy administrating! 🚀**
