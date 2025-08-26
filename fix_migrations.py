#!/usr/bin/env python
"""
Script to force Django migrations creation and application
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sda_admin.settings')
    django.setup()
    
    print("=== SDA Models Migration Fix ===")
    
    print("\n1. Removing any old migration files...")
    migrations_dir = "sda_models/migrations"
    if os.path.exists(migrations_dir):
        for file in os.listdir(migrations_dir):
            if file.startswith('0') and file.endswith('.py'):
                os.remove(os.path.join(migrations_dir, file))
                print(f"   Removed: {file}")
    
    print("\n2. Creating fresh migrations for sda_models...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'sda_models', '--verbosity=2'])
    except Exception as e:
        print(f"Error creating migrations: {e}")
        sys.exit(1)
    
    print("\n3. Applying migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', 'sda_models', '--verbosity=2'])
    except Exception as e:
        print(f"Error applying migrations: {e}")
        sys.exit(1)
    
    print("\n4. Showing final migration status...")
    execute_from_command_line(['manage.py', 'showmigrations', 'sda_models'])
    
    print("\n=== Migration Fix Completed Successfully! ===")
    print("Your Django admin panel should now show all SDA models.")
