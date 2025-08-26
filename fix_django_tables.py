#!/usr/bin/env python
"""
Script to create Django's built-in tables (auth, sessions, etc.)
without affecting existing SDA tables.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sda_admin.settings')
    django.setup()

def check_table_exists(table_name):
    """Check if a table exists in the database"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name = %s
            );
        """, [table_name])
        return cursor.fetchone()[0]

def main():
    setup_django()
    
    # Check if Django's built-in tables exist
    django_tables = [
        'django_migrations',
        'django_session',
        'auth_user',
        'auth_group',
        'auth_permission',
        'django_content_type',
        'django_admin_log'
    ]
    
    missing_tables = []
    for table in django_tables:
        if not check_table_exists(table):
            missing_tables.append(table)
    
    if missing_tables:
        print(f"Missing Django tables: {missing_tables}")
        print("Creating Django's built-in tables...")
        
        # Run migrations for Django's built-in apps only
        execute_from_command_line(['manage.py', 'migrate', 'auth'])
        execute_from_command_line(['manage.py', 'migrate', 'contenttypes'])
        execute_from_command_line(['manage.py', 'migrate', 'sessions'])
        execute_from_command_line(['manage.py', 'migrate', 'admin'])
        
        print("Django tables created successfully!")
    else:
        print("All Django tables already exist.")
    
    # Create superuser if it doesn't exist
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        print("Creating admin user...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Admin user created! Username: admin, Password: admin123")
    else:
        print("Admin user already exists.")

if __name__ == '__main__':
    main()
