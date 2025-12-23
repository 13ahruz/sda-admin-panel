"""
Django models that mirror the FastAPI SQLAlchemy models.
These models use managed=False to avoid Django trying to create tables.
"""
from django.db import models
from django.contrib.postgres.fields import ArrayField


class TimestampMixin(models.Model):
    """Base mixin for created_at and updated_at fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ==================== Projects ====================

class PropertySector(TimestampMixin):
    """Property Sectors model"""
    # Multilingual fields
    title_en = models.TextField(null=True, blank=True)
    title_az = models.TextField(null=True, blank=True)
    title_ru = models.TextField(null=True, blank=True)
    
    description_en = models.TextField(null=True, blank=True)
    description_az = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    
    # Legacy fields
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    # Featured projects
    featured_project_1_id = models.IntegerField(null=True, blank=True, db_column='featured_project_1_id')
    featured_project_2_id = models.IntegerField(null=True, blank=True, db_column='featured_project_2_id')
    featured_project_3_id = models.IntegerField(null=True, blank=True, db_column='featured_project_3_id')
    
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'property_sectors'
        ordering = ['order']
        verbose_name = 'Property Sector'
        verbose_name_plural = 'Property Sectors'

    def __str__(self):
        return self.title_en or self.title or f"Sector {self.id}"


class SectorInn(TimestampMixin):
    """Sector Inns (features) model"""
    property_sector = models.ForeignKey(
        PropertySector, 
        on_delete=models.CASCADE, 
        related_name='inns',
        db_column='property_sector_id'
    )
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'sector_inns'
        ordering = ['property_sector', 'order']
        verbose_name = 'Sector Inn'
        verbose_name_plural = 'Sector Inns'

    def __str__(self):
        return self.title


class PropertySectorProcess(TimestampMixin):
    """Property Sector Process Steps model"""
    property_sector = models.ForeignKey(
        PropertySector,
        on_delete=models.CASCADE,
        related_name='process_steps',
        db_column='property_sector_id'
    )
    
    # Multilingual title fields
    title_en = models.TextField(null=True, blank=True)
    title_az = models.TextField(null=True, blank=True)
    title_ru = models.TextField(null=True, blank=True)
    
    # Multilingual description fields
    description_en = models.TextField(null=True, blank=True)
    description_az = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    
    # Legacy fields
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'property_sector_processes'
        ordering = ['property_sector', 'order']
        verbose_name = 'Property Sector Process Step'
        verbose_name_plural = 'Property Sector Process Steps'

    def __str__(self):
        return self.title_en or self.title or f"Process {self.id}"


class Project(TimestampMixin):
    """Projects model"""
    # Multilingual fields
    title_en = models.TextField(null=True, blank=True)
    title_az = models.TextField(null=True, blank=True)
    title_ru = models.TextField(null=True, blank=True)
    
    description_en = models.TextField(null=True, blank=True)
    description_az = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    
    about_project_en = models.TextField(null=True, blank=True)
    about_project_az = models.TextField(null=True, blank=True)
    about_project_ru = models.TextField(null=True, blank=True)
    
    # Legacy fields
    title = models.TextField(null=True, blank=True)
    
    slug = models.TextField(unique=True, null=True, blank=True)
    tag = models.TextField(null=True, blank=True)
    client = models.TextField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    property_sector = models.ForeignKey(
        PropertySector, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='projects',
        db_column='property_sector_id'
    )
    cover_photo_url = models.TextField(null=True, blank=True)
    services = models.ManyToManyField(
        'Service',
        through='ProjectService',
        related_name='projects',
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'projects'
        ordering = ['-year', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title_en or self.title or f"Project {self.id}"


class ProjectService(models.Model):
    """Association table for Project-Service many-to-many relationship"""
    id = models.AutoField(primary_key=True)  # Add explicit primary key
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, db_column='service_id')
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'project_services'
        ordering = ['order']

    def __str__(self):
        return f"{self.project} - {self.service}"


class ProjectSolution(TimestampMixin):
    """Project Solutions model"""
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='solutions',
        db_column='project_id'
    )
    
    # Multilingual title fields
    title_en = models.TextField(null=True, blank=True)
    title_az = models.TextField(null=True, blank=True)
    title_ru = models.TextField(null=True, blank=True)
    
    # Multilingual description fields
    description_en = models.TextField(null=True, blank=True)
    description_az = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'project_solutions'
        ordering = ['project', 'order']
        verbose_name = 'Project Delivered Solution'
        verbose_name_plural = 'Project Delivered Solutions'

    def __str__(self):
        return self.title_en or f"Solution {self.id}"


class ProjectPhoto(TimestampMixin):
    """Project Photos model"""
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='photos',
        db_column='project_id'
    )
    image_url = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'project_photos'
        ordering = ['project', 'order']
        verbose_name = 'Project Photo'
        verbose_name_plural = 'Project Photos'

    def __str__(self):
        return f"Photo for {self.project}"


# ==================== News ====================

class News(TimestampMixin):
    """News model"""
    photo_url = models.TextField(null=True, blank=True)
    tags = ArrayField(models.TextField(), default=list, blank=True)
    
    # Multilingual fields
    title = models.TextField()
    title_en = models.TextField(null=True, blank=True)
    title_az = models.TextField(null=True, blank=True)
    title_ru = models.TextField(null=True, blank=True)
    
    summary = models.TextField(null=True, blank=True)
    summary_en = models.TextField(null=True, blank=True)
    summary_az = models.TextField(null=True, blank=True)
    summary_ru = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'news'
        ordering = ['-created_at']
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'

    def __str__(self):
        return self.title_en or self.title or f"News {self.id}"


class NewsSection(TimestampMixin):
    """News Sections model"""
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='sections',
        db_column='news_id'
    )
    order = models.IntegerField(default=0)
    
    # Multilingual fields
    heading = models.TextField(null=True, blank=True)
    heading_en = models.TextField(null=True, blank=True)
    heading_az = models.TextField(null=True, blank=True)
    heading_ru = models.TextField(null=True, blank=True)
    
    content = models.TextField(null=True, blank=True)
    content_en = models.TextField(null=True, blank=True)
    content_az = models.TextField(null=True, blank=True)
    content_ru = models.TextField(null=True, blank=True)
    
    image_url = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'news_sections'
        ordering = ['news', 'order']
        verbose_name = 'News Section'
        verbose_name_plural = 'News Sections'

    def __str__(self):
        return f"Section {self.order} of {self.news}"


# ==================== Team ====================

class TeamMember(TimestampMixin):
    """Team Members model"""
    # Multilingual fields
    full_name_en = models.TextField(null=True, blank=True)
    full_name_az = models.TextField(null=True, blank=True)
    full_name_ru = models.TextField(null=True, blank=True)
    
    role_en = models.TextField(null=True, blank=True)
    role_az = models.TextField(null=True, blank=True)
    role_ru = models.TextField(null=True, blank=True)
    
    bio_en = models.TextField(null=True, blank=True)
    bio_az = models.TextField(null=True, blank=True)
    bio_ru = models.TextField(null=True, blank=True)
    
    photo_url = models.TextField(null=True, blank=True)
    linkedin_url = models.TextField(null=True, blank=True)
    
    # Legacy fields
    full_name = models.TextField(null=True, blank=True)
    role = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'team_members'
        ordering = ['id']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return self.full_name_en or self.full_name or f"Member {self.id}"


class TeamSection(TimestampMixin):
    """Team Sections model"""
    title = models.TextField()
    button_text = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'team_sections'
        ordering = ['id']
        verbose_name = 'Team Section'
        verbose_name_plural = 'Team Sections'

    def __str__(self):
        return self.title


class TeamSectionItem(TimestampMixin):
    """Team Section Items model"""
    team_section = models.ForeignKey(
        TeamSection,
        on_delete=models.CASCADE,
        related_name='items',
        db_column='team_section_id'
    )
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    photo_url = models.TextField(null=True, blank=True)
    button_text = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'team_section_items'
        ordering = ['team_section', 'order']
        verbose_name = 'Team Section Item'
        verbose_name_plural = 'Team Section Items'

    def __str__(self):
        return self.name


# ==================== Services ====================

class Service(TimestampMixin):
    """Services model"""
    # Multilingual fields
    name_en = models.TextField(null=True, blank=True)
    name_az = models.TextField(null=True, blank=True)
    name_ru = models.TextField(null=True, blank=True)
    
    description_en = models.TextField(null=True, blank=True)
    description_az = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    
    hero_text_en = models.TextField(null=True, blank=True)
    hero_text_az = models.TextField(null=True, blank=True)
    hero_text_ru = models.TextField(null=True, blank=True)
    
    meta_title_en = models.TextField(null=True, blank=True)
    meta_title_az = models.TextField(null=True, blank=True)
    meta_title_ru = models.TextField(null=True, blank=True)
    
    meta_description_en = models.TextField(null=True, blank=True)
    meta_description_az = models.TextField(null=True, blank=True)
    meta_description_ru = models.TextField(null=True, blank=True)
    
    # Legacy fields
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    hero_text = models.TextField(null=True, blank=True)
    meta_title = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    
    slug = models.CharField(max_length=255, unique=True)
    image_url = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)
    icon_url = models.TextField(null=True, blank=True)
    
    # Featured projects
    featured_project_1 = models.ForeignKey(
        'Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='featured_in_service_1',
        db_column='featured_project_1_id'
    )
    featured_project_2 = models.ForeignKey(
        'Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='featured_in_service_2',
        db_column='featured_project_2_id'
    )

    class Meta:
        managed = False
        db_table = 'services'
        ordering = ['order']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name_en or self.name or f"Service {self.id}"


class ServiceBenefit(TimestampMixin):
    """Service Benefits model"""
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='benefits', db_column='service_id')
    
    # Multilingual title fields
    title_en = models.TextField(null=True, blank=True)
    title_az = models.TextField(null=True, blank=True)
    title_ru = models.TextField(null=True, blank=True)
    
    # Multilingual description fields
    description_en = models.TextField(null=True, blank=True)
    description_az = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    
    # Legacy fields
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'service_benefits'
        ordering = ['order']
        verbose_name = 'Service Benefit'
        verbose_name_plural = 'Service Benefits'

    def __str__(self):
        return self.title_en or self.title or f"Benefit {self.id}"


class ServiceProcess(TimestampMixin):
    """Service Process Steps model (What We Do section with icons)"""
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='process_steps', db_column='service_id')
    
    # Multilingual title fields
    title_en = models.TextField(null=True, blank=True)
    title_az = models.TextField(null=True, blank=True)
    title_ru = models.TextField(null=True, blank=True)
    
    # Multilingual description fields
    description_en = models.TextField(null=True, blank=True)
    description_az = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    
    # Legacy fields
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    # Icon URL
    icon_url = models.TextField(null=True, blank=True)
    
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'service_processes'
        ordering = ['order']
        verbose_name = 'Service What We Do Item'
        verbose_name_plural = 'Service What We Do Items'

    def __str__(self):
        return self.title_en or self.title or f"Process {self.id}"


class ServiceWorkProcess(TimestampMixin):
    """Service Work Process Steps model (numbered Process section without icons)"""
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='work_process_steps', db_column='service_id')
    
    # Multilingual title fields
    title_en = models.TextField(null=True, blank=True)
    title_az = models.TextField(null=True, blank=True)
    title_ru = models.TextField(null=True, blank=True)
    
    # Multilingual description fields
    description_en = models.TextField(null=True, blank=True)
    description_az = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    
    # Legacy fields
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'service_work_processes'
        ordering = ['order']
        verbose_name = 'Service Process Step'
        verbose_name_plural = 'Service Process Steps'

    def __str__(self):
        return self.title_en or self.title or f"Work Process {self.id}"


# ==================== About ====================

class About(TimestampMixin):
    """About model"""
    # Simple numeric fields (no multilingual needed for numbers)
    years_experience = models.IntegerField(default=0)
    ongoing_projects = models.IntegerField(default=0)
    team_members = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'about'
        verbose_name = 'About Section'
        verbose_name_plural = 'About Sections'

    def __str__(self):
        return f"About Section (Experience: {self.years_experience}+ years)"


# ==================== Contact ===================

class ContactMessage(TimestampMixin):
    """Contact Messages model"""
    # Contact form fields
    name = models.TextField(null=True, blank=True)
    
    # Careers form fields
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    
    phone_number = models.TextField()
    email = models.TextField()
    message = models.TextField(null=True, blank=True)
    cv_url = models.TextField(null=True, blank=True)
    
    # Additional contact form fields
    company = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    property_type = models.TextField(null=True, blank=True)
    
    # Status tracking
    is_read = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='new')

    class Meta:
        managed = False
        db_table = 'contact_messages'
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name or self.first_name} - {self.email}"


# ==================== Partners ====================

class Partner(TimestampMixin):
    """Partners model"""
    title = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'partners'
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return self.title or f"Partner {self.id}"


class PartnerLogo(TimestampMixin):
    """Partner Logos model"""
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='logos',
        db_column='partner_id'
    )
    image_url = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'partner_logos'
        ordering = ['partner', 'order']
        verbose_name = 'Partner Logo'
        verbose_name_plural = 'Partner Logos'

    def __str__(self):
        return f"Logo for {self.partner}"


# ==================== Work Process ====================

class WorkProcess(TimestampMixin):
    """Work Processes model"""
    # Multilingual fields
    title_en = models.TextField(null=True, blank=True)
    title_az = models.TextField(null=True, blank=True)
    title_ru = models.TextField(null=True, blank=True)
    
    description_en = models.TextField(null=True, blank=True)
    description_az = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    
    # Legacy fields
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    order = models.IntegerField(default=0)
    image_url = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'work_processes'
        ordering = ['order']
        verbose_name = 'Work Process'
        verbose_name_plural = 'Work Processes'

    def __str__(self):
        return self.title_en or self.title or f"Process {self.id}"


# ==================== Approaches ====================

class Approach(TimestampMixin):
    """Approaches model"""
    # Multilingual fields
    title_en = models.TextField(null=True, blank=True)
    title_az = models.TextField(null=True, blank=True)
    title_ru = models.TextField(null=True, blank=True)
    
    description_en = models.TextField(null=True, blank=True)
    description_az = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    
    # Legacy fields
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'approaches'
        ordering = ['order']
        verbose_name = 'Approach'
        verbose_name_plural = 'Approaches'

    def __str__(self):
        return self.title_en or self.title or f"Approach {self.id}"
