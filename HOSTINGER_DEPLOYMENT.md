# Hostinger Deployment Guide for SDA Django Admin Panel

## Prerequisites
- Hostinger hosting account with Python support
- Access to your hosting control panel
- FTP/SFTP access to upload files

## Step 1: Prepare Your Environment File

Copy your production `.env` file from your FastAPI backend or create a new one:

```env
# Database Configuration (same as your FastAPI backend)
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_SERVER=your_postgres_host
POSTGRES_PORT=5432
POSTGRES_DB=sda_db

# Django Settings for Production
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here-change-this
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,admin.yourdomain.com

# Static and Media Files
STATIC_URL=/static/
STATIC_ROOT=/home/username/public_html/admin/static/
MEDIA_URL=/media/
MEDIA_ROOT=/home/username/public_html/admin/media/
```

## Step 2: Upload Files to Hostinger

1. Upload all files from the `admin-panel` folder to your hosting directory
2. You can create a subdirectory like `/public_html/admin/` for the admin panel
3. Make sure all Python files are uploaded with correct permissions

## Step 3: Install Dependencies

SSH into your Hostinger account or use the terminal in control panel:

```bash
cd /path/to/your/admin/panel
pip install -r requirements.txt --user
```

## Step 4: Configure Database

Ensure your PostgreSQL database is accessible from your hosting environment. Update the `.env` file with the correct database credentials provided by Hostinger.

## Step 5: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Step 6: Create Admin User

```bash
python manage.py create_admin --username admin --email your-email@domain.com --password your-secure-password
```

Or create manually:
```bash
python manage.py createsuperuser
```

## Step 7: Configure Web Server

### Option A: Using .htaccess (if Apache)

Create a `.htaccess` file in your admin directory:

```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ wsgi.py [QSA,L]

# Static files
Alias /static/ /path/to/your/static/files/
<Directory "/path/to/your/static/files/">
    Require all granted
</Directory>

# Media files
Alias /media/ /path/to/your/media/files/
<Directory "/path/to/your/media/files/">
    Require all granted
</Directory>
```

### Option B: Using Hostinger's Python App Setup

1. Go to your Hostinger control panel
2. Navigate to "Advanced" → "Python App"
3. Create a new Python application
4. Set the entry point to `sda_admin.wsgi:application`
5. Set the Python version to 3.8 or higher
6. Configure environment variables

## Step 8: Test the Installation

1. Visit `https://yourdomain.com/admin/` (or your configured URL)
2. Log in with your admin credentials
3. Verify that all models are visible and accessible

## Step 9: Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` set
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] HTTPS enabled for admin panel
- [ ] Database credentials secured
- [ ] Admin user has strong password
- [ ] Regular backups configured

## Troubleshooting

### Common Issues:

1. **500 Internal Server Error**
   - Check error logs in Hostinger control panel
   - Verify database connectivity
   - Ensure all dependencies are installed

2. **Static Files Not Loading**
   - Run `collectstatic` command
   - Check static file paths in settings
   - Verify web server configuration

3. **Database Connection Error**
   - Verify database credentials in `.env`
   - Check if PostgreSQL is accessible from your hosting
   - Ensure database exists and has proper permissions

4. **Permission Denied Errors**
   - Check file permissions (644 for files, 755 for directories)
   - Ensure Python has write access to media directory

### Getting Help:

1. Check Hostinger documentation for Python apps
2. Review Django deployment documentation
3. Check error logs for specific error messages
4. Contact Hostinger support for hosting-specific issues

## Maintenance

### Regular Tasks:
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Backup database regularly
- Monitor admin access logs
- Update Django and security patches

### Updating Content:
- Use the admin panel to manage all content
- Changes are immediately reflected in your FastAPI backend
- No need to restart services for content changes
