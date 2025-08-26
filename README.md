# SDA Django Admin Panel

This Django admin panel provides a web interface to manage the content of your SDA FastAPI backend. It connects to the same PostgreSQL database and allows you to manage all your data through Django's powerful admin interface.

## Features

- **Complete Content Management**: Manage all SDA models including About, Projects, News, Team, Services, etc.
- **Import/Export**: Built-in data import/export functionality for key models
- **Image Previews**: Visual previews of images in the admin interface
- **Inline Editing**: Edit related objects (like photos, logos) directly within parent objects
- **Search & Filtering**: Advanced search and filtering capabilities
- **Responsive Interface**: Works on desktop and mobile devices

## Models Managed

- **About**: Company information and logos
- **Projects**: Project portfolio with photos and categories
- **News**: News articles with sections and images
- **Team**: Team members and team sections
- **Services**: Service offerings and benefits
- **Partners**: Partner information and logos
- **Property Sectors**: Real estate sectors and inns
- **Approaches**: Company approaches
- **Work Processes**: Workflow information
- **Contact Messages**: Contact form submissions

## Installation & Deployment

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Update the `.env` file with your database credentials:

```env
# Database Configuration (same as FastAPI backend)
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_SERVER=your_postgres_host
POSTGRES_PORT=5432
POSTGRES_DB=sda_db

# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run the Application

For development:
```bash
python manage.py runserver 0.0.0.0:8001
```

For production, configure your web server (Apache/Nginx) to serve the Django application.

## Hostinger Deployment

1. Upload all files to your Hostinger hosting directory
2. Install Python dependencies using pip
3. Configure your database settings in `.env`
4. Set up a subdomain or directory for the admin panel
5. Configure your web server to run the Django application
6. Create a superuser account
7. Access the admin panel at `https://yourdomain.com/admin/`

## Database Integration

This admin panel uses the same PostgreSQL database as your FastAPI backend. It does NOT create or modify the database schema - it only manages the existing data. The models are mapped to the existing tables created by your FastAPI application.

## Security Considerations

- Always set `DEBUG=False` in production
- Use a strong `SECRET_KEY`
- Restrict `ALLOWED_HOSTS` to your actual domains
- Use HTTPS in production
- Regularly update dependencies
- Limit admin access to authorized personnel only

## Admin Interface Features

### Content Management
- **Projects**: Manage project portfolio with cover images and photo galleries
- **News**: Create and manage news articles with multiple sections
- **Team**: Manage team members and organizational sections
- **Services**: Configure service offerings and benefits

### Media Management
- Image preview in list views
- Direct image URL management
- Order management for galleries and collections

### Data Import/Export
- Export data to Excel/CSV formats
- Import data from external sources
- Bulk operations support

## Troubleshooting

### Database Connection Issues
- Verify database credentials in `.env`
- Ensure PostgreSQL is running and accessible
- Check firewall settings for database access

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check static file configuration in settings
- Verify web server static file serving

### Permission Errors
- Ensure proper file permissions on the hosting server
- Check directory ownership and access rights

## Support

For issues related to the admin panel, check:
1. Django logs for error messages
2. Database connectivity
3. Environment variable configuration
4. Static file serving setup
