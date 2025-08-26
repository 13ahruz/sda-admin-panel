# WSGI configuration for production deployment
# This file can be used with Apache mod_wsgi or other WSGI servers

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add your project directory to the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_path)

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sda_admin.settings')

# Get the WSGI application
application = get_wsgi_application()
