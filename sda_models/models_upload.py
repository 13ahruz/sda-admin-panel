from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
import os


def upload_to_about_logos(instance, filename):
    """Upload path for about logos"""
    return f'about/logos/{filename}'

def upload_to_services(instance, filename):
    """Upload path for service images"""
    return f'services/{filename}'

def upload_to_partners(instance, filename):
    """Upload path for partner logos"""
    return f'partners/{filename}'

def upload_to_projects(instance, filename):
    """Upload path for project images"""
    return f'projects/{filename}'

def upload_to_news(instance, filename):
    """Upload path for news images"""
    return f'news/{filename}'

def upload_to_team(instance, filename):
    """Upload path for team photos"""
    return f'team/{filename}'


class TimestampMixin(models.Model):
    """Mixin for created_at and updated_at fields to match SQLAlchemy backend"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


# About models with file upload support
class About(TimestampMixin):
    """About section model - matches backend About model"""
    experience = models.TextField()
    project_count = models.TextField()
    members = models.TextField()
    
    class Meta:
        db_table = 'about'
        verbose_name = 'About'
        verbose_name_plural = 'About'
    
    def __str__(self):
        return f"About - Experience: {self.experience[:50]}"


class AboutLogo(TimestampMixin):
    """About logos model with file upload support"""
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='logos')
    # File upload field for admin
    image_file = models.ImageField(upload_to=upload_to_about_logos, blank=True, null=True)
    # URL field for backend compatibility
    image_url = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'about_logos'
        verbose_name = 'About Logo'
        verbose_name_plural = 'About Logos'
        indexes = [
            models.Index(fields=['about', 'order'], name='ix_about_logos_about_order'),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generate URL from uploaded file
        if self.image_file and not self.image_url:
            self.image_url = f"{settings.MEDIA_URL}{self.image_file}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"About Logo {self.order}"


# Services models with file upload support
class Service(TimestampMixin):
    """Service model with file upload support"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    # File upload field for admin
    image_file = models.ImageField(upload_to=upload_to_services, blank=True, null=True)
    # URL field for backend compatibility
    image_url = models.TextField(blank=True)
    
    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def save(self, *args, **kwargs):
        # Auto-generate URL from uploaded file
        if self.image_file and not self.image_url:
            self.image_url = f"{settings.MEDIA_URL}{self.image_file}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


# Partners models with file upload support
class Partner(TimestampMixin):
    """Partner model with file upload support"""
    name = models.CharField(max_length=255)
    website_url = models.URLField(blank=True, null=True)
    # File upload field for admin
    logo_file = models.ImageField(upload_to=upload_to_partners, blank=True, null=True)
    # URL field for backend compatibility
    logo_url = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'partners'
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        indexes = [
            models.Index(fields=['order'], name='ix_partners_order'),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generate URL from uploaded file
        if self.logo_file and not self.logo_url:
            self.logo_url = f"{settings.MEDIA_URL}{self.logo_file}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


# Projects models with file upload support
class Project(TimestampMixin):
    """Project model with file upload support"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    # File upload field for admin
    cover_image_file = models.ImageField(upload_to=upload_to_projects, blank=True, null=True)
    # URL field for backend compatibility
    cover_image_url = models.TextField(blank=True)
    
    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
    
    def save(self, *args, **kwargs):
        # Auto-generate URL from uploaded file
        if self.cover_image_file and not self.cover_image_url:
            self.cover_image_url = f"{settings.MEDIA_URL}{self.cover_image_file}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class ProjectImage(TimestampMixin):
    """Project images model with file upload support"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    # File upload field for admin
    image_file = models.ImageField(upload_to=upload_to_projects, blank=True, null=True)
    # URL field for backend compatibility
    image_url = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'project_images'
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'
        indexes = [
            models.Index(fields=['project', 'order'], name='ix_project_images_project_order'),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generate URL from uploaded file
        if self.image_file and not self.image_url:
            self.image_url = f"{settings.MEDIA_URL}{self.image_file}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.project.title} - Image {self.order}"


# News models with file upload support
class News(TimestampMixin):
    """News model with file upload support"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    # File upload field for admin
    image_file = models.ImageField(upload_to=upload_to_news, blank=True, null=True)
    # URL field for backend compatibility
    image_url = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'news'
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # Auto-generate URL from uploaded file
        if self.image_file and not self.image_url:
            self.image_url = f"{settings.MEDIA_URL}{self.image_file}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


# Team models with file upload support
class Team(TimestampMixin):
    """Team member model with file upload support"""
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    # File upload field for admin
    photo_file = models.ImageField(upload_to=upload_to_team, blank=True, null=True)
    # URL field for backend compatibility
    photo_url = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'team'
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
        indexes = [
            models.Index(fields=['order'], name='ix_team_order'),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generate URL from uploaded file
        if self.photo_file and not self.photo_url:
            self.photo_url = f"{settings.MEDIA_URL}{self.photo_file}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.position}"


# Property Sectors model
class PropertySector(TimestampMixin):
    """Property sector model"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'property_sectors'
        verbose_name = 'Property Sector'
        verbose_name_plural = 'Property Sectors'
        indexes = [
            models.Index(fields=['order'], name='ix_property_sectors_order'),
        ]
    
    def __str__(self):
        return self.title


# Approaches model
class Approach(TimestampMixin):
    """Approach model"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'approaches'
        verbose_name = 'Approach'
        verbose_name_plural = 'Approaches'
        indexes = [
            models.Index(fields=['order'], name='ix_approaches_order'),
        ]
    
    def __str__(self):
        return self.title


# Work Process model
class WorkProcess(TimestampMixin):
    """Work process model"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    step_number = models.IntegerField()
    
    class Meta:
        db_table = 'work_process'
        verbose_name = 'Work Process Step'
        verbose_name_plural = 'Work Process Steps'
        indexes = [
            models.Index(fields=['step_number'], name='ix_work_process_step_number'),
        ]
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


# Contact model
class Contact(TimestampMixin):
    """Contact submission model"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'contact'
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'}"
