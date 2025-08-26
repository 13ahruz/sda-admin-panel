import os
import uuid
from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage
from django.conf import settings


def upload_to_projects_covers(instance, filename):
    """Upload path for project cover photos"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"projects/covers/{filename}"


def upload_to_projects_photos(instance, filename):
    """Upload path for project photos"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"projects/photos/{filename}"


def upload_to_partners_logos(instance, filename):
    """Upload path for partner logos"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"partners/logos/{filename}"


def upload_to_about_logos(instance, filename):
    """Upload path for about logos"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"about/logos/{filename}"


def upload_to_team_members(instance, filename):
    """Upload path for team member photos"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"team/members/{filename}"


def upload_to_team_sections(instance, filename):
    """Upload path for team section items"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"team/sections/{filename}"


def upload_to_services(instance, filename):
    """Upload path for service icons"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"services/{filename}"


def upload_to_news(instance, filename):
    """Upload path for news images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"news/{filename}"


def upload_to_work_processes(instance, filename):
    """Upload path for work process images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"work-processes/{filename}"


class TimestampMixin(models.Model):
    """Mixin for created_at and updated_at fields"""
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PropertySector(TimestampMixin):
    """Property sectors model"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'property_sectors'
        verbose_name = 'Property Sector'
        verbose_name_plural = 'Property Sectors'

    def __str__(self):
        return self.name


class Project(TimestampMixin):
    """Projects model"""
    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=100, blank=True, null=True)
    client = models.CharField(max_length=200, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    property_sector = models.ForeignKey(PropertySector, on_delete=models.SET_NULL, related_name='projects', null=True, blank=True)
    
    # URL field matching backend database structure exactly
    cover_photo_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title


class ProjectPhoto(TimestampMixin):
    """Project photos model"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='photos')
    
    # URL field matching backend database structure exactly
    image_url = models.URLField()
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'project_photos'
        verbose_name = 'Project Photo'
        verbose_name_plural = 'Project Photos'
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} - Photo {self.order}"


class Partner(TimestampMixin):
    """Partners model"""
    title = models.CharField(max_length=200)
    button_text = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'partners'
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return self.title


class PartnerLogo(TimestampMixin):
    """Partner logos model"""
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='logos')
    
    # URL field matching backend database structure exactly
    image_url = models.URLField()
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'partner_logos'
        verbose_name = 'Partner Logo'
        verbose_name_plural = 'Partner Logos'
        ordering = ['order']

    def __str__(self):
        return f"{self.partner.title} - Logo {self.order}"


class About(TimestampMixin):
    """About sections model"""
    experience = models.CharField(max_length=100)
    project_count = models.CharField(max_length=100)
    members = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'about'
        verbose_name = 'About Section'
        verbose_name_plural = 'About Sections'

    def __str__(self):
        return f"About - {self.experience} experience"


class AboutLogo(TimestampMixin):
    """About logos model"""
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='logos')
    
    # File field for logo
    image = models.ImageField(upload_to=upload_to_about_logos, blank=True, null=True)
    # URL field (automatically populated from file)
    image_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'about_logos'
        verbose_name = 'About Logo'
        verbose_name_plural = 'About Logos'
        ordering = ['order']

    def __str__(self):
        return f"About Logo {self.order}"

    def save(self, *args, **kwargs):
        if self.image:
            self.image_url = f"/uploads/{self.image.name}"
        super().save(*args, **kwargs)


class Service(TimestampMixin):
    """Services model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # File field for icon
    icon = models.ImageField(upload_to=upload_to_services, blank=True, null=True)
    # URL field (automatically populated from file)
    icon_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.icon:
            self.icon_url = f"/uploads/{self.icon.name}"
        super().save(*args, **kwargs)


class ServiceBenefit(TimestampMixin):
    """Service benefits model"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='benefits')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'service_benefits'
        verbose_name = 'Service Benefit'
        verbose_name_plural = 'Service Benefits'
        ordering = ['order']

    def __str__(self):
        return f"{self.service.title} - {self.title}"


class News(TimestampMixin):
    """News model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # File field for image
    image = models.ImageField(upload_to=upload_to_news, blank=True, null=True)
    # URL field (automatically populated from file)
    image_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'news'
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            self.image_url = f"/uploads/{self.image.name}"
        super().save(*args, **kwargs)


class TeamMember(TimestampMixin):
    """Team members model"""
    full_name = models.CharField(max_length=200)
    role = models.CharField(max_length=100, blank=True, null=True)
    
    # File field for photo
    photo = models.ImageField(upload_to=upload_to_team_members, blank=True, null=True)
    # URL field (automatically populated from file)
    photo_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'team_members'
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.photo:
            self.photo_url = f"/uploads/{self.photo.name}"
        super().save(*args, **kwargs)


class TeamSection(TimestampMixin):
    """Team sections model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'team_sections'
        verbose_name = 'Team Section'
        verbose_name_plural = 'Team Sections'
        ordering = ['order']

    def __str__(self):
        return self.title


class TeamSectionItem(TimestampMixin):
    """Team section items model"""
    team_section = models.ForeignKey(TeamSection, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # File field for photo
    photo = models.ImageField(upload_to=upload_to_team_sections, blank=True, null=True)
    # URL field (automatically populated from file)
    photo_url = models.URLField(blank=True, null=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'team_section_items'
        verbose_name = 'Team Section Item'
        verbose_name_plural = 'Team Section Items'
        ordering = ['display_order']

    def __str__(self):
        return f"{self.team_section.title} - {self.name}"

    def save(self, *args, **kwargs):
        if self.photo:
            self.photo_url = f"/uploads/{self.photo.name}"
        super().save(*args, **kwargs)


class WorkProcess(TimestampMixin):
    """Work processes model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # File field for image
    image = models.ImageField(upload_to=upload_to_work_processes, blank=True, null=True)
    # URL field (automatically populated from file)
    photo_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'work_processes'
        verbose_name = 'Work Process'
        verbose_name_plural = 'Work Processes'
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            self.photo_url = f"/uploads/{self.image.name}"
        super().save(*args, **kwargs)


class Approach(TimestampMixin):
    """Approaches model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'approaches'
        verbose_name = 'Approach'
        verbose_name_plural = 'Approaches'
        ordering = ['order']

    def __str__(self):
        return self.title


class ContactMessage(TimestampMixin):
    """Contact message model - matches backend ContactMessage model"""
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    cv_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'contact_messages'  # This is the actual table name in backend
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
