# SDA Admin Panel

Django-based admin panel for managing the SDA Consulting FastAPI backend database.

## Features

- **Complete Database Management**: Manage all backend tables through a user-friendly interface
- **Multilingual Support**: Edit content in English, Azerbaijani, and Russian
- **Inline Editing**: Edit related models (photos, sections, logos) within parent records
- **Advanced Filtering**: Filter records by various criteria
- **Image Previews**: View uploaded images directly in the admin interface
- **Status Management**: Track and manage contact messages and their statuses
- **Bulk Actions**: Perform actions on multiple records at once

## Models Managed

### Content Models
- **Projects**: Project portfolio with photos, sectors, and multilingual content
- **News**: News articles with sections and multilingual support
- **Services**: Service listings with benefits and SEO metadata
- **Team Members**: Team profiles with LinkedIn integration

### Configuration Models
- **Property Sectors**: Property sector categories with inns (features)
- **Work Processes**: Company work process steps
- **Approaches**: Company approach methodology
- **About**: Company information and statistics
- **Partners**: Partner logos and information

### Communication
- **Contact Messages**: Contact form and career applications with status tracking

## Installation

### Local Development

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set environment variables**:
Create a `.env` file in the admin-panel directory:
```env
# Database Configuration (same as FastAPI backend)
POSTGRES_DB=sda_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432

# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Media Files (path to backend uploads folder)
MEDIA_ROOT=../sda/uploads
```

3. **Run migrations** (Django will inspect existing database):
```bash
python manage.py migrate
```

4. **Create superuser**:
```bash
python manage.py createsuperuser
```

5. **Run the development server**:
```bash
python manage.py runserver 8001
```

6. **Access the admin panel**:
Open http://localhost:8001/admin/ and login with your superuser credentials.

### Docker Deployment

1. **Build and run with Docker Compose**:
```bash
docker-compose up -d
```

2. **Create superuser in container**:
```bash
docker-compose exec admin-panel python manage.py createsuperuser
```

3. **Access the admin panel**:
Open http://localhost:8001/admin/

## Database Connection

The admin panel connects to the **same PostgreSQL database** as your FastAPI backend. All models use `managed=False` which means:
- Django won't create or modify tables
- Django only reads and updates existing data
- Your FastAPI backend remains the source of truth for database schema

## Usage Guide

### Managing Projects

1. Navigate to **Projects** in the admin
2. Click **Add Project** or edit an existing one
3. Fill in multilingual fields (English, Azerbaijani, Russian)
4. Add photos using the inline photo section
5. Set property sector, client, year, and tags
6. Save the project

### Managing News Articles

1. Go to **News Articles**
2. Create a new article or edit existing
3. Add title, summary, and photo
4. Add sections with headings, content, and optional images
5. Set tags for categorization

### Managing Contact Messages

1. View all messages in **Contact Messages**
2. Filter by status (new, in progress, resolved) or type (contact/career)
3. Use bulk actions to mark as read/unread
4. Update status as you process messages
5. View CV uploads for career applications

### Managing Team Members

1. Navigate to **Team Members**
2. Add member with multilingual name, role, and bio
3. Upload photo and add LinkedIn URL
4. Save to display on website

### Managing Services

1. Go to **Services**
2. Add service with slug (URL-friendly identifier)
3. Fill multilingual name, description, hero text
4. Add SEO metadata (meta title/description)
5. Set order for display sequence
6. Upload icon and image

## File Uploads

The admin panel displays images uploaded through the FastAPI backend. The `MEDIA_ROOT` setting should point to the FastAPI uploads directory (default: `../sda/uploads`).

Image uploads should be handled through the FastAPI backend API, not directly through Django admin to maintain consistency.

## Security

### Production Deployment

Before deploying to production:

1. **Set strong SECRET_KEY**:
```env
DJANGO_SECRET_KEY=generate-a-strong-random-secret-key
```

2. **Disable DEBUG**:
```env
DEBUG=False
```

3. **Set ALLOWED_HOSTS**:
```env
ALLOWED_HOSTS=your-domain.com,your-ip-address
```

4. **Use HTTPS**: Configure your web server (nginx/Apache) to use SSL
5. **Set strong superuser password**
6. **Restrict admin access**: Consider IP whitelisting or VPN

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists and is accessible

### Images Not Displaying
- Check `MEDIA_ROOT` path in settings
- Verify uploads directory permissions
- Ensure images exist in the uploads folder

### Permission Errors
- Make sure superuser account is created
- Check database user has sufficient privileges

## Maintenance

### Backup Database
```bash
pg_dump -U postgres sda_db > backup.sql
```

### View Logs
```bash
# Docker
docker-compose logs -f admin-panel

# Local
Check console output where manage.py runserver is running
```

## Support

For issues or questions, contact the development team.

## Version

- Django: 4.2.x
- Python: 3.10+
- PostgreSQL: 14+
