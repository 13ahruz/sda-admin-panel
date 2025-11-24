# 📋 Admin Panel Setup Checklist

## Pre-Setup Verification

### Prerequisites Check
- [ ] Python 3.10 or higher installed
- [ ] PostgreSQL 14+ installed and running
- [ ] FastAPI backend already set up with database
- [ ] Database `sda_db` exists and is accessible
- [ ] pip or pip3 available

### Verify FastAPI Backend
```powershell
# Check if backend database is running
psql -U postgres -d sda_db -c "\dt"
```

Expected tables should include:
- projects, project_photos
- news, news_sections
- team_members
- services
- contact_messages
- ... and more

## Setup Process

### Step 1: Navigate to Admin Panel
```powershell
cd c:\Users\BSShabili\Desktop\sda\admin-panel
```

- [ ] Confirmed in admin-panel directory

### Step 2: Create Environment File
```powershell
Copy-Item .env.example .env
```

Then edit `.env` file:
```env
POSTGRES_DB=sda_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432

DJANGO_SECRET_KEY=django-insecure-change-this-in-production-key-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,153.92.223.91

MEDIA_ROOT=../sda/uploads
```

- [ ] .env file created
- [ ] Database credentials match your FastAPI backend
- [ ] MEDIA_ROOT points to correct uploads directory

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

Wait for installation to complete...

- [ ] All dependencies installed successfully
- [ ] No error messages

### Step 4: Test Database Connection
```powershell
python test_connection.py
```

You should see:
```
✓ SUCCESS - Database connection
✓ SUCCESS - Table access
Found X tables:
  ✓ projects
  ✓ news
  ✓ team_members
  ...
```

- [ ] Database connection successful
- [ ] All expected tables found

### Step 5: Run Migrations
```powershell
python manage.py migrate
```

This applies Django's internal migrations (auth, sessions, etc.)
Your existing tables remain untouched.

- [ ] Migrations completed successfully
- [ ] No errors reported

### Step 6: Collect Static Files
```powershell
python manage.py collectstatic --noinput
```

This gathers admin interface CSS/JS files.

- [ ] Static files collected
- [ ] staticfiles/ directory created

### Step 7: Create Superuser
```powershell
python manage.py createsuperuser
```

You'll be prompted for:
- Username: (choose your admin username)
- Email: (your email)
- Password: (strong password)
- Password (again): (confirm)

**Important:** Remember these credentials!

- [ ] Superuser created successfully
- [ ] Credentials saved securely

### Step 8: Start Development Server
```powershell
python manage.py runserver 8001
```

You should see:
```
Starting development server at http://127.0.0.1:8001/
Quit the server with CTRL-BREAK.
```

- [ ] Server started successfully
- [ ] No error messages

### Step 9: Access Admin Panel
Open browser to: **http://localhost:8001/admin/**

- [ ] Admin login page displays
- [ ] Login with superuser credentials
- [ ] Successfully logged in

### Step 10: Verify Admin Interface

Check that all models are visible in admin:

**Content Management:**
- [ ] Projects
- [ ] Project Photos  
- [ ] Property Sectors
- [ ] Sector Inns

**News & Blog:**
- [ ] News Articles
- [ ] News Sections

**Team:**
- [ ] Team Members
- [ ] Team Sections
- [ ] Team Section Items

**Services:**
- [ ] Services
- [ ] Service Benefits

**About & Partners:**
- [ ] About Sections
- [ ] About Logos
- [ ] Partners
- [ ] Partner Logos

**Process & Approach:**
- [ ] Work Processes
- [ ] Approaches

**Communications:**
- [ ] Contact Messages

## Functionality Testing

### Test 1: View Existing Data
- [ ] Click on "Projects"
- [ ] See existing projects from database
- [ ] Projects display correct titles and data

### Test 2: Edit Existing Record
- [ ] Click on a project
- [ ] See all multilingual fields (EN, AZ, RU)
- [ ] See inline photos
- [ ] Make a small change
- [ ] Save successfully

### Test 3: Create New Record
- [ ] Click "Add Project"
- [ ] Fill required fields
- [ ] Add inline photo
- [ ] Save successfully
- [ ] New project appears in list

### Test 4: Image Previews
- [ ] Open project with photos
- [ ] See photo previews in inline section
- [ ] Previews display correctly

### Test 5: Filtering & Search
- [ ] Use filter sidebar (property sector, year)
- [ ] Search for project by name
- [ ] Results filter correctly

### Test 6: Contact Messages
- [ ] Open Contact Messages
- [ ] Filter by status
- [ ] Mark message as read
- [ ] Update status
- [ ] Changes save correctly

### Test 7: Multilingual Content
- [ ] Open any record with multilingual fields
- [ ] See organized fieldsets (English, Azərbaycan, Русский)
- [ ] Edit fields in different languages
- [ ] Save successfully

## Troubleshooting Checks

### If Database Connection Fails:
- [ ] PostgreSQL service is running
- [ ] Database credentials in .env are correct
- [ ] Database `sda_db` exists
- [ ] User has proper permissions

### If Images Don't Display:
- [ ] MEDIA_ROOT path is correct
- [ ] Uploads directory exists at that path
- [ ] Files exist in uploads directory
- [ ] Path uses forward slashes or escaped backslashes

### If Can't Login:
- [ ] Superuser was created successfully
- [ ] Using correct username and password
- [ ] No typos in credentials

### If Port 8001 In Use:
- [ ] Check what's using port: `netstat -ano | findstr :8001`
- [ ] Stop other process or use different port
- [ ] Run with: `python manage.py runserver 8002`

## Production Deployment Checklist

### Security
- [ ] Change DJANGO_SECRET_KEY to strong random value
- [ ] Set DEBUG=False
- [ ] Update ALLOWED_HOSTS with your domain
- [ ] Use strong superuser password
- [ ] Enable HTTPS/SSL

### Configuration
- [ ] Database credentials secured
- [ ] Environment variables set
- [ ] Firewall configured
- [ ] Backup strategy in place

### Testing
- [ ] All functionality tested
- [ ] Performance acceptable
- [ ] Security audit completed
- [ ] Documentation reviewed

### Deployment
- [ ] Choose deployment method (Docker/Manual)
- [ ] Follow DEPLOYMENT.md guide
- [ ] Configure reverse proxy (nginx)
- [ ] Setup SSL certificate
- [ ] Configure monitoring
- [ ] Test in production environment

## Docker Setup Checklist (Alternative)

### Prerequisites
- [ ] Docker installed
- [ ] Docker Compose installed

### Setup Steps
```powershell
cd admin-panel

# Copy environment file
Copy-Item .env.example .env

# Edit .env with your settings
notepad .env

# Build and start
docker-compose up -d

# Create superuser
docker-compose exec admin-panel python manage.py createsuperuser

# Access admin
# Open http://localhost:8001/admin/
```

- [ ] Containers running
- [ ] Superuser created
- [ ] Admin accessible

## Post-Setup Tasks

### Documentation
- [ ] Read README.md
- [ ] Review QUICKSTART.md
- [ ] Bookmark DEPLOYMENT.md for later

### Team Onboarding
- [ ] Create admin accounts for team members
- [ ] Document workflows
- [ ] Train team on admin usage
- [ ] Setup support process

### Maintenance
- [ ] Setup regular backups
- [ ] Plan update schedule
- [ ] Monitor performance
- [ ] Review logs regularly

## Success Criteria

✅ Admin panel accessible at http://localhost:8001/admin/
✅ Can login with superuser credentials
✅ All models visible and accessible
✅ Can view existing database records
✅ Can create, edit, delete records
✅ Inline editing works (photos, sections)
✅ Image previews display correctly
✅ Multilingual fields organized properly
✅ Filtering and search work
✅ Changes persist in database
✅ No errors in console
✅ Performance is acceptable

## Final Verification

Run through this checklist:
- [ ] Admin panel is running
- [ ] All models are accessible
- [ ] Data displays correctly
- [ ] Can perform CRUD operations
- [ ] Images load properly
- [ ] No console errors
- [ ] FastAPI backend still works
- [ ] Frontend displays data correctly

## Next Steps After Setup

1. **Explore the Interface**
   - Navigate through all models
   - Familiarize yourself with layout
   - Test different features

2. **Start Managing Content**
   - Update existing records
   - Add new content
   - Upload images
   - Manage contact messages

3. **Plan for Production**
   - Review security settings
   - Plan deployment strategy
   - Setup monitoring
   - Configure backups

4. **Train Your Team**
   - Create user guides
   - Hold training sessions
   - Document workflows
   - Setup support

## Resources

- **Main Documentation**: README.md
- **Quick Start**: QUICKSTART.md
- **Production Guide**: DEPLOYMENT.md
- **Architecture**: ARCHITECTURE.md
- **Overview**: START_HERE.md

## Support

If you encounter issues:
1. Check troubleshooting section above
2. Review relevant documentation
3. Check console/logs for errors
4. Test database connection
5. Verify environment variables

---

## 🎉 Congratulations!

If all items are checked, your admin panel is:
- ✅ Fully installed
- ✅ Properly configured
- ✅ Working correctly
- ✅ Ready to use

**Happy content managing! 🚀**
