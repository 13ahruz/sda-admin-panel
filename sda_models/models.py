from django.db import models
from django.utils import timezone



class TimestampMixin(models.Model):
    """Mixin for created_at and updated_at fields"""
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PropertySector(TimestampMixin):
    """Property sectors model"""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'property_sectors'
        verbose_name = 'Property Sector'
        verbose_name_plural = 'Property Sectors'
        ordering = ['order']

    def __str__(self):
        return self.title


class SectorInn(TimestampMixin):
    """Sector inn model"""
    property_sector = models.ForeignKey(PropertySector, on_delete=models.CASCADE, related_name='inns')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'sector_inns'
        verbose_name = 'Sector Inn'
        verbose_name_plural = 'Sector Inns'
        ordering = ['property_sector', 'order']
        constraints = [
            models.UniqueConstraint(
                fields=['property_sector', 'title'],
                name='uq_sector_inns_sector_title'
            )
        ]

    def __str__(self):
        return f"{self.property_sector.title} - {self.title}"


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
    
    # URL field matching backend database structure exactly
    image_url = models.URLField()
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'about_logos'
        verbose_name = 'About Logo'
        verbose_name_plural = 'About Logos'
        ordering = ['order']

    def __str__(self):
        return f"About Logo {self.order}"


class Service(TimestampMixin):
    """Services model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # URL field matching backend database structure exactly
    icon_url = models.URLField()
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['order']

    def __str__(self):
        return self.title


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
    
    # URL field matching backend database structure exactly
    image_url = models.URLField()
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'news'
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TeamMember(TimestampMixin):
    """Team members model"""
    full_name = models.CharField(max_length=200)
    role = models.CharField(max_length=100, blank=True, null=True)
    
    # URL field matching backend database structure exactly
    photo_url = models.URLField()

    class Meta:
        db_table = 'team_members'
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return self.full_name


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
    
    # URL field matching backend database structure exactly
    photo_url = models.URLField()
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'team_section_items'
        verbose_name = 'Team Section Item'
        verbose_name_plural = 'Team Section Items'
        ordering = ['display_order']

    def __str__(self):
        return f"{self.team_section.title} - {self.name}"


class WorkProcess(TimestampMixin):
    """Work processes model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # URL field matching backend database structure exactly
    image_url = models.URLField()
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'work_processes'
        verbose_name = 'Work Process'
        verbose_name_plural = 'Work Processes'
        ordering = ['order']

    def __str__(self):
        return self.title


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
