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
    # Multilingual experience fields
    experience_en = models.TextField(blank=True, null=True)
    experience_az = models.TextField(blank=True, null=True)
    experience_ru = models.TextField(blank=True, null=True)
    
    # Multilingual project count fields
    project_count_en = models.TextField(blank=True, null=True)
    project_count_az = models.TextField(blank=True, null=True)
    project_count_ru = models.TextField(blank=True, null=True)
    
    # Multilingual members fields
    members_en = models.TextField(blank=True, null=True)
    members_az = models.TextField(blank=True, null=True)
    members_ru = models.TextField(blank=True, null=True)
    
    # Legacy fields
    experience = models.TextField(blank=True, null=True)
    project_count = models.TextField(blank=True, null=True)
    members = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'about'
        verbose_name = 'About'
        verbose_name_plural = 'About'
    
    def __str__(self):
        return f"About - Experience: {self.experience_en or self.experience or 'N/A'}"


class AboutLogo(TimestampMixin):
    """About logos model - matches backend AboutLogo model"""
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='logos')
    image_url = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'about_logos'
        verbose_name = 'About Logo'
        verbose_name_plural = 'About Logos'
        ordering = ['order']
        indexes = [
            models.Index(fields=['about', 'order'], name='ix_about_logos_about_order'),
        ]
    
    def __str__(self):
        return f"About Logo {self.order}"


class PropertySector(TimestampMixin):
    """Property sectors model"""
    # Multilingual title fields
    title_en = models.TextField(blank=True, null=True, help_text="Sector title (English)")
    title_az = models.TextField(blank=True, null=True, help_text="Sector title (Azerbaijani)")
    title_ru = models.TextField(blank=True, null=True, help_text="Sector title (Russian)")
    
    # Multilingual description fields
    description_en = models.TextField(blank=True, null=True, help_text="Sector description (English)")
    description_az = models.TextField(blank=True, null=True, help_text="Sector description (Azerbaijani)")
    description_ru = models.TextField(blank=True, null=True, help_text="Sector description (Russian)")
    
    # Legacy fields
    title = models.TextField(blank=True, null=True, help_text="Legacy title")
    description = models.TextField(blank=True, null=True, help_text="Legacy description")
    
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'property_sectors'
        verbose_name = 'Property Sector'
        verbose_name_plural = 'Property Sectors'
        ordering = ['order']
    
    def __str__(self):
        return self.title_en or self.title or f"Sector {self.id}"


class SectorInn(TimestampMixin):
    """Sector inns model"""
    property_sector = models.ForeignKey(PropertySector, on_delete=models.CASCADE, related_name='inns')
    title = models.TextField(help_text="Inn title")
    description = models.TextField(blank=True, null=True, help_text="Inn description")
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'sector_inns'
        verbose_name = 'Sector Inn'
        verbose_name_plural = 'Sector Inns'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.title} ({self.property_sector.title})"


class Project(TimestampMixin):
    """Projects model"""
    # Multilingual title fields
    title_en = models.TextField(blank=True, null=True, help_text="Project title (English)")
    title_az = models.TextField(blank=True, null=True, help_text="Project title (Azerbaijani)")
    title_ru = models.TextField(blank=True, null=True, help_text="Project title (Russian)")
    
    # Multilingual description fields
    description_en = models.TextField(blank=True, null=True, help_text="Project description (English)")
    description_az = models.TextField(blank=True, null=True, help_text="Project description (Azerbaijani)")
    description_ru = models.TextField(blank=True, null=True, help_text="Project description (Russian)")
    
    # Legacy title field
    title = models.TextField(blank=True, null=True, help_text="Legacy title")
    
    # Slug for URL-friendly identification
    slug = models.TextField(blank=True, null=True, unique=True, help_text="URL slug")
    
    tag = models.TextField(blank=True, null=True, help_text="Project tag")
    client = models.TextField(blank=True, null=True, help_text="Client name")
    year = models.IntegerField(blank=True, null=True, help_text="Project year")
    property_sector = models.ForeignKey(
        PropertySector, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='projects'
    )
    cover_photo_url = models.TextField(blank=True, null=True, help_text="Cover photo URL")
    
    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-year', 'title']
    
    def __str__(self):
        return self.title_en or self.title or f"Project {self.id}"


class ProjectPhoto(TimestampMixin):
    """Project photos model"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='photos')
    image_url = models.TextField(blank=True, help_text="Photo URL")
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'project_photos'
        verbose_name = 'Project Photo'
        verbose_name_plural = 'Project Photos'
        ordering = ['order']
    
    def __str__(self):
        return f"Photo {self.order} for {self.project.title}"


class News(TimestampMixin):
    """News articles model"""
    # Multilingual title fields
    title = models.TextField(help_text="Default News title")
    title_en = models.TextField(blank=True, null=True, help_text="News title (English)")
    title_az = models.TextField(blank=True, null=True, help_text="News title (Azerbaijani)")
    title_ru = models.TextField(blank=True, null=True, help_text="News title (Russian)")
    
    # Multilingual summary fields
    summary = models.TextField(blank=True, null=True, help_text="Default summary")
    summary_en = models.TextField(blank=True, null=True, help_text="News summary (English)")
    summary_az = models.TextField(blank=True, null=True, help_text="News summary (Azerbaijani)")
    summary_ru = models.TextField(blank=True, null=True, help_text="News summary (Russian)")
    
    photo_url = models.TextField(blank=True, null=True, help_text="News photo URL")
    tags = ArrayField(models.TextField(), blank=True, default=list, help_text="News tags")
    
    class Meta:
        db_table = 'news'
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title_en or self.title


class NewsSection(TimestampMixin):
    """News sections model"""
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='sections')
    order = models.IntegerField(default=0, help_text="Section order")
    
    # Multilingual heading fields
    heading = models.TextField(blank=True, null=True, help_text="Default heading")
    heading_en = models.TextField(blank=True, null=True, help_text="Section heading (English)")
    heading_az = models.TextField(blank=True, null=True, help_text="Section heading (Azerbaijani)")
    heading_ru = models.TextField(blank=True, null=True, help_text="Section heading (Russian)")
    
    # Multilingual content fields
    content = models.TextField(blank=True, null=True, help_text="Default content")
    content_en = models.TextField(blank=True, null=True, help_text="Section content (English)")
    content_az = models.TextField(blank=True, null=True, help_text="Section content (Azerbaijani)")
    content_ru = models.TextField(blank=True, null=True, help_text="Section content (Russian)")
    
    image_url = models.TextField(blank=True, null=True, help_text="Section image URL")
    
    class Meta:
        db_table = 'news_sections'
        verbose_name = 'News Section'
        verbose_name_plural = 'News Sections'
        ordering = ['order']
    
    def __str__(self):
        heading_text = self.heading_en or self.heading or "No heading"
        return f"Section {self.order} - {self.news.title} - {heading_text}"


class TeamMember(TimestampMixin):
    """Team members model"""
    # Multilingual full name fields
    full_name_en = models.TextField(blank=True, null=True, help_text="Full name (English)")
    full_name_az = models.TextField(blank=True, null=True, help_text="Full name (Azerbaijani)")
    full_name_ru = models.TextField(blank=True, null=True, help_text="Full name (Russian)")
    
    # Multilingual role fields
    role_en = models.TextField(blank=True, null=True, help_text="Role/Position (English)")
    role_az = models.TextField(blank=True, null=True, help_text="Role/Position (Azerbaijani)")
    role_ru = models.TextField(blank=True, null=True, help_text="Role/Position (Russian)")
    
    # Multilingual bio fields
    bio_en = models.TextField(blank=True, null=True, help_text="Bio (English)")
    bio_az = models.TextField(blank=True, null=True, help_text="Bio (Azerbaijani)")
    bio_ru = models.TextField(blank=True, null=True, help_text="Bio (Russian)")
    
    photo_url = models.TextField(blank=True, null=True, help_text="Photo URL")
    linkedin_url = models.TextField(blank=True, null=True, help_text="LinkedIn profile URL")
    
    # Legacy fields
    full_name = models.TextField(blank=True, null=True, help_text="Legacy full name")
    role = models.TextField(blank=True, null=True, help_text="Legacy role")
    bio = models.TextField(blank=True, null=True, help_text="Legacy bio")
    
    class Meta:
        db_table = 'team_members'
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
        ordering = ['full_name']
    
    def __str__(self):
        return self.full_name_en or self.full_name or f"Team Member {self.id}"


class TeamSection(TimestampMixin):
    """Team sections model"""
    title = models.TextField(help_text="Section title")
    button_text = models.TextField(blank=True, null=True, help_text="Button text")
    
    class Meta:
        db_table = 'team_sections'
        verbose_name = 'Team Section'
        verbose_name_plural = 'Team Sections'
    
    def __str__(self):
        return self.title


class TeamSectionItem(TimestampMixin):
    """Team section items model"""
    team_section = models.ForeignKey(TeamSection, on_delete=models.CASCADE, related_name='items')
    name = models.TextField(help_text="Item name")
    description = models.TextField(blank=True, null=True, help_text="Item description")
    photo_url = models.TextField(blank=True, null=True, help_text="Photo URL")
    button_text = models.TextField(blank=True, null=True, help_text="Button text")
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'team_section_items'
        verbose_name = 'Team Section Item'
        verbose_name_plural = 'Team Section Items'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} ({self.team_section.title})"


class Service(TimestampMixin):
    """Services model"""
    # Multilingual name/title fields
    name_en = models.TextField(blank=True, null=True, help_text="Service name (English)")
    name_az = models.TextField(blank=True, null=True, help_text="Service name (Azerbaijani)")
    name_ru = models.TextField(blank=True, null=True, help_text="Service name (Russian)")
    
    # Multilingual description fields
    description_en = models.TextField(blank=True, null=True, help_text="Service description (English)")
    description_az = models.TextField(blank=True, null=True, help_text="Service description (Azerbaijani)")
    description_ru = models.TextField(blank=True, null=True, help_text="Service description (Russian)")
    
    # Multilingual hero text fields
    hero_text_en = models.TextField(blank=True, null=True, help_text="Hero text (English)")
    hero_text_az = models.TextField(blank=True, null=True, help_text="Hero text (Azerbaijani)")
    hero_text_ru = models.TextField(blank=True, null=True, help_text="Hero text (Russian)")
    
    # Multilingual meta fields
    meta_title_en = models.TextField(blank=True, null=True, help_text="Meta title (English)")
    meta_title_az = models.TextField(blank=True, null=True, help_text="Meta title (Azerbaijani)")
    meta_title_ru = models.TextField(blank=True, null=True, help_text="Meta title (Russian)")
    
    meta_description_en = models.TextField(blank=True, null=True, help_text="Meta description (English)")
    meta_description_az = models.TextField(blank=True, null=True, help_text="Meta description (Azerbaijani)")
    meta_description_ru = models.TextField(blank=True, null=True, help_text="Meta description (Russian)")
    
    # Legacy fields
    name = models.TextField(blank=True, null=True, help_text="Legacy name")
    description = models.TextField(blank=True, null=True, help_text="Legacy description")
    hero_text = models.TextField(blank=True, null=True, help_text="Legacy hero text")
    meta_title = models.TextField(blank=True, null=True, help_text="Legacy meta title")
    meta_description = models.TextField(blank=True, null=True, help_text="Legacy meta description")
    
    slug = models.CharField(max_length=255, unique=True, help_text="URL slug")
    image_url = models.TextField(blank=True, null=True, help_text="Service image URL")
    order = models.IntegerField(default=0, help_text="Display order")
    icon_url = models.TextField(blank=True, null=True, help_text="Icon URL")
    
    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['order']
    
    def __str__(self):
        return self.name_en or self.name or f"Service {self.id}"


class ServiceBenefit(TimestampMixin):
    """Service benefits model"""
    title = models.TextField(help_text="Benefit title")
    description = models.TextField(blank=True, null=True, help_text="Benefit description")
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'service_benefits'
        verbose_name = 'Service Benefit'
        verbose_name_plural = 'Service Benefits'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class ContactMessage(TimestampMixin):
    """Contact messages model"""
    first_name = models.TextField(help_text="First name")
    last_name = models.TextField(help_text="Last name")
    phone_number = models.TextField(help_text="Phone number")
    email = models.TextField(help_text="Email address")
    message = models.TextField(blank=True, null=True, help_text="Message content")
    cv_url = models.TextField(blank=True, null=True, help_text="CV file URL")
    
    class Meta:
        db_table = 'contact_messages'
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class Approach(TimestampMixin):
    """Approaches model"""
    # Multilingual title fields
    title_en = models.TextField(blank=True, null=True, help_text="Approach title (English)")
    title_az = models.TextField(blank=True, null=True, help_text="Approach title (Azerbaijani)")
    title_ru = models.TextField(blank=True, null=True, help_text="Approach title (Russian)")
    
    # Multilingual description fields
    description_en = models.TextField(blank=True, null=True, help_text="Approach description (English)")
    description_az = models.TextField(blank=True, null=True, help_text="Approach description (Azerbaijani)")
    description_ru = models.TextField(blank=True, null=True, help_text="Approach description (Russian)")
    
    # Legacy fields
    title = models.TextField(blank=True, null=True, help_text="Legacy title")
    description = models.TextField(blank=True, null=True, help_text="Legacy description")
    
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'approaches'
        verbose_name = 'Approach'
        verbose_name_plural = 'Approaches'
        ordering = ['order']
    
    def __str__(self):
        return self.title_en or self.title or f"Approach {self.id}"


class Partner(TimestampMixin):
    """Partners model"""
    # Multilingual title fields
    title_en = models.TextField(blank=True, null=True, help_text="Partner title (English)")
    title_az = models.TextField(blank=True, null=True, help_text="Partner title (Azerbaijani)")
    title_ru = models.TextField(blank=True, null=True, help_text="Partner title (Russian)")
    
    # Multilingual button text fields
    button_text_en = models.TextField(blank=True, null=True, help_text="Button text (English)")
    button_text_az = models.TextField(blank=True, null=True, help_text="Button text (Azerbaijani)")
    button_text_ru = models.TextField(blank=True, null=True, help_text="Button text (Russian)")
    
    # Legacy fields
    title = models.TextField(blank=True, null=True, help_text="Legacy title")
    button_text = models.TextField(blank=True, null=True, help_text="Legacy button text")
    
    class Meta:
        db_table = 'partners'
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
    
    def __str__(self):
        return self.title_en or self.title or f"Partner {self.id}"


class PartnerLogo(TimestampMixin):
    """Partner logos model"""
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='logos')
    image_url = models.TextField(help_text="Logo image URL")
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'partner_logos'
        verbose_name = 'Partner Logo'
        verbose_name_plural = 'Partner Logos'
        ordering = ['order']
    
    def __str__(self):
        partner_title = self.partner.title_en or self.partner.title or "Unknown Partner"
        return f"Logo {self.order} for {partner_title}"


class WorkProcess(TimestampMixin):
    """Work processes model"""
    # Multilingual title fields
    title_en = models.TextField(blank=True, null=True, help_text="Work process title (English)")
    title_az = models.TextField(blank=True, null=True, help_text="Work process title (Azerbaijani)")
    title_ru = models.TextField(blank=True, null=True, help_text="Work process title (Russian)")
    
    # Multilingual description fields
    description_en = models.TextField(blank=True, null=True, help_text="Process description (English)")
    description_az = models.TextField(blank=True, null=True, help_text="Process description (Azerbaijani)")
    description_ru = models.TextField(blank=True, null=True, help_text="Process description (Russian)")
    
    # Legacy fields
    title = models.TextField(blank=True, null=True, help_text="Legacy title")
    description = models.TextField(blank=True, null=True, help_text="Legacy description")
    
    order = models.IntegerField(default=0, help_text="Display order")
    image_url = models.TextField(blank=True, null=True, help_text="Process image URL")
    
    class Meta:
        db_table = 'work_processes'
        verbose_name = 'Work Process'
        verbose_name_plural = 'Work Processes'
        ordering = ['order']
    
    def __str__(self):
        return self.title_en or self.title or f"Work Process {self.id}"
