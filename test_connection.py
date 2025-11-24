"""
Database connection test script.
Run this to verify admin panel can connect to the database.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_panel.settings')
django.setup()

from django.db import connection
from django.conf import settings

def test_database_connection():
    """Test database connection"""
    print("=" * 60)
    print("SDA Admin Panel - Database Connection Test")
    print("=" * 60)
    
    print("\nDatabase Configuration:")
    print(f"  Name: {settings.DATABASES['default']['NAME']}")
    print(f"  User: {settings.DATABASES['default']['USER']}")
    print(f"  Host: {settings.DATABASES['default']['HOST']}")
    print(f"  Port: {settings.DATABASES['default']['PORT']}")
    
    print("\nTesting connection...", end=" ")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print("✓ SUCCESS")
            print(f"\nPostgreSQL Version: {version[0]}")
    except Exception as e:
        print("✗ FAILED")
        print(f"\nError: {e}")
        return False
    
    print("\nTesting table access...", end=" ")
    try:
        with connection.cursor() as cursor:
            # Check if projects table exists
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            print("✓ SUCCESS")
            print(f"\nFound {len(tables)} tables:")
            
            expected_tables = [
                'about', 'about_logos', 'approaches', 'contact_messages',
                'news', 'news_sections', 'partner_logos', 'partners',
                'project_photos', 'projects', 'property_sectors',
                'sector_inns', 'service_benefits', 'services',
                'team_members', 'team_section_items', 'team_sections',
                'work_processes'
            ]
            
            found_tables = [t[0] for t in tables]
            
            for table in expected_tables:
                if table in found_tables:
                    print(f"  ✓ {table}")
                else:
                    print(f"  ✗ {table} (missing)")
            
    except Exception as e:
        print("✗ FAILED")
        print(f"\nError: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("Database connection test completed successfully!")
    print("=" * 60)
    print("\nYou can now:")
    print("  1. Create a superuser: python manage.py createsuperuser")
    print("  2. Run the server: python manage.py runserver 8001")
    print("  3. Access admin: http://localhost:8001/admin/")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = test_database_connection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
