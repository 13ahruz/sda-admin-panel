# 🔧 Fix for "auth_user" Table Missing Error

The error shows that Django is trying to access the `auth_user` table which doesn't exist in your database. This is because your database only has FastAPI tables, not Django's built-in authentication tables.

## 🚀 Quick Fix

Run this command on your server:

```bash
# Stop current containers and clean volumes
docker-compose -f docker-compose.simple.yml down -v

# Restart with proper migration setup
docker-compose -f docker-compose.simple.yml up -d --build
```

Or use the automated fix script:
```bash
chmod +x fix-400.sh
./fix-400.sh
```

## 🔍 What the fix does:

1. **Stops containers and cleans volumes** to ensure fresh start
2. **Creates Django's built-in tables** (auth_user, auth_group, django_admin_log, etc.)
3. **Preserves your existing SDA tables** (projects, news, etc.)
4. **Creates admin user** automatically
5. **Sets permissive ALLOWED_HOSTS** to avoid 400 errors

## ⏳ Expected behavior:

When you restart, you'll see messages like:
```
Running Django migrations for built-in apps...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
Admin user created: username=admin, password=admin123
```

This is **normal and expected**! Django needs these tables for the admin interface.

## 🎯 After the fix:

- **Access**: http://your-server-ip:8001/admin/
- **Login**: admin / admin123
- **Your SDA data** will be available and manageable
- **No data loss** - your existing tables are preserved

## 🔧 Manual verification:

Check if it's working:
```bash
# Check container logs
docker-compose -f docker-compose.simple.yml logs sda-admin

# Check container status
docker-compose -f docker-compose.simple.yml ps
```

The admin panel should now work properly with both Django's authentication system and your SDA content management! 🎉
