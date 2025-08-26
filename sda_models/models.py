from django.db import models
from django.contrib.postgres.fields import ArrayField


class TimestampMixin(models.Model):
    """Mixin for created_at and updated_at fields to match SQLAlchemy backend"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


# About models - exact match to FastAPI backend
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
    """About logos model - matches backend AboutLogo model"""
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='logos')
    image_url = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'about_logos'
        verbose_name = 'About Logo'
        verbose_name_plural = 'About Logos'
        indexes = [
            models.Index(fields=['about', 'order'], name='ix_about_logos_about_order'),
        ]
    
    def __str__(self):
        return f"About Logo {self.order}"


# Services models - exact match to FastAPI backend
class Service(TimestampMixin):
    """Service model - matches backend Service model"""
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)
    icon_url = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        indexes = [
            models.Index(fields=['order'], name='ix_services_order'),
        ]
    
    def __str__(self):
        return self.name


class ServiceBenefit(TimestampMixin):
    """Service benefit model - matches backend ServiceBenefit model"""
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'service_benefits'
        verbose_name = 'Service Benefit'
        verbose_name_plural = 'Service Benefits'
        indexes = [
            models.Index(fields=['order'], name='ix_service_benefits_order'),
        ]
    
    def __str__(self):
        return self.title


# Approaches model - exact match to FastAPI backend
class Approach(TimestampMixin):
    """Approach model - matches backend Approach model"""
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
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


# Contact model - exact match to FastAPI backend
class ContactMessage(TimestampMixin):
    """Contact message model - matches backend ContactMessage model"""
    first_name = models.TextField()
    last_name = models.TextField()
    phone_number = models.TextField()
    email = models.TextField()
    message = models.TextField(null=True, blank=True)
    cv_url = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'contact_messages'
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        indexes = [
            models.Index(fields=['created_at'], name='ix_contact_messages_created_at'),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


# News models - exact match to FastAPI backend
class News(TimestampMixin):
    """News model - matches backend News model"""
    photo_url = models.TextField(null=True, blank=True)
    tags = ArrayField(models.TextField(), default=list, blank=True)
    title = models.TextField()
    summary = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'news'
        verbose_name = 'News'
        verbose_name_plural = 'News'
        indexes = [
            models.Index(fields=['created_at'], name='ix_news_created_at'),
        ]
    
    def __str__(self):
        return self.title


class NewsSection(TimestampMixin):
    """News section model - matches backend NewsSection model"""
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='sections')
    order = models.IntegerField(default=0)
    heading = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'news_sections'
        verbose_name = 'News Section'
        verbose_name_plural = 'News Sections'
        indexes = [
            models.Index(fields=['news', 'order'], name='ix_news_sections_news_order'),
        ]
    
    def __str__(self):
        return f"{self.news.title} - Section {self.order}"


# Partners models - exact match to FastAPI backend
class Partner(TimestampMixin):
    """Partner model - matches backend Partner model"""
    title = models.TextField()
    button_text = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'partners'
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
    
    def __str__(self):
        return self.title


class PartnerLogo(TimestampMixin):
    """Partner logo model - matches backend PartnerLogo model"""
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='logos')
    image_url = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'partner_logos'
        verbose_name = 'Partner Logo'
        verbose_name_plural = 'Partner Logos'
        indexes = [
            models.Index(fields=['partner', 'order'], name='ix_partner_logos_partner_order'),
        ]
    
    def __str__(self):
        return f"{self.partner.title} - Logo {self.order}"


# Property Sectors models - exact match to FastAPI backend
class PropertySector(TimestampMixin):
    """Property sector model - matches backend PropertySector model"""
    title = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True)
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


class SectorInn(TimestampMixin):
    """Sector inn model - matches backend SectorInn model"""
    property_sector = models.ForeignKey(PropertySector, on_delete=models.CASCADE, related_name='inns')
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'sector_inns'
        verbose_name = 'Sector Inn'
        verbose_name_plural = 'Sector Inns'
        constraints = [
            models.UniqueConstraint(fields=['property_sector', 'title'], name='uq_sector_inns_sector_title'),
        ]
        indexes = [
            models.Index(fields=['property_sector', 'order'], name='ix_sector_inns_sector_order'),
        ]
    
    def __str__(self):
        return f"{self.property_sector.title} - {self.title}"


# Projects models - exact match to FastAPI backend
class Project(TimestampMixin):
    """Project model - matches backend Project model"""
    title = models.TextField()
    tag = models.TextField(null=True, blank=True)
    client = models.TextField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    property_sector = models.ForeignKey(PropertySector, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    cover_photo_url = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['property_sector'], name='ix_projects_property_sector'),
            models.Index(fields=['year'], name='ix_projects_year'),
            models.Index(fields=['tag'], name='ix_projects_tag'),
        ]
    
    def __str__(self):
        return self.title


class ProjectPhoto(TimestampMixin):
    """Project photo model - matches backend ProjectPhoto model"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='photos')
    image_url = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'project_photos'
        verbose_name = 'Project Photo'
        verbose_name_plural = 'Project Photos'
        indexes = [
            models.Index(fields=['project', 'order'], name='ix_project_photos_proj_order'),
        ]
    
    def __str__(self):
        return f"{self.project.title} - Photo {self.order}"


# Team models - exact match to FastAPI backend
class TeamMember(TimestampMixin):
    """Team member model - matches backend TeamMember model"""
    full_name = models.TextField()
    role = models.TextField(null=True, blank=True)
    photo_url = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'team_members'
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
        indexes = [
            models.Index(fields=['full_name'], name='ix_team_members_full_name'),
        ]
    
    def __str__(self):
        return self.full_name


class TeamSection(TimestampMixin):
    """Team section model - matches backend TeamSection model"""
    title = models.TextField()
    button_text = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'team_sections'
        verbose_name = 'Team Section'
        verbose_name_plural = 'Team Sections'
    
    def __str__(self):
        return self.title


class TeamSectionItem(TimestampMixin):
    """Team section item model - matches backend TeamSectionItem model"""
    team_section = models.ForeignKey(TeamSection, on_delete=models.CASCADE, related_name='items')
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    photo_url = models.TextField(null=True, blank=True)
    button_text = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'team_section_items'
        verbose_name = 'Team Section Item'
        verbose_name_plural = 'Team Section Items'
        indexes = [
            models.Index(fields=['team_section', 'order'], name='ix_team_section_items_order'),
        ]
    
    def __str__(self):
        return f"{self.team_section.title} - {self.name}"


# Work Process model - exact match to FastAPI backend
class WorkProcess(TimestampMixin):
    """Work process model - matches backend WorkProcess model"""
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)
    image_url = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'work_processes'
        verbose_name = 'Work Process'
        verbose_name_plural = 'Work Processes'
        indexes = [
            models.Index(fields=['order'], name='ix_work_processes_order'),
        ]
    
    def __str__(self):
        return self.title
