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
    
    print("Creating migrations for sda_models...")
    execute_from_command_line(['manage.py', 'makemigrations', 'sda_models', '--verbosity=2'])
    
    print("\nApplying migrations...")
    execute_from_command_line(['manage.py', 'migrate', 'sda_models', '--verbosity=2'])
    
    print("\nMigrations completed!")
