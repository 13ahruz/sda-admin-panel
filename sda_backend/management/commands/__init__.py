"""
Custom Django management commands can be placed here.

Example usage:
    python manage.py your_command_name

To create a new command:
1. Create a file in this directory (e.g., export_data.py)
2. Define a Command class that extends BaseCommand
3. Implement handle() method

Example:

from django.core.management.base import BaseCommand
from sda_backend.models import Project

class Command(BaseCommand):
    help = 'Export all projects to JSON'

    def handle(self, *args, **options):
        projects = Project.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Found {projects.count()} projects'))
"""
