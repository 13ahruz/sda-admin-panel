from django.db import models
from django.contrib.postgres.fields import ArrayField


# Upload function definitions
def upload_to_project_covers(instance, filename):
    return f"projects/covers/{filename}"

def upload_to_project_photos(instance, filename):
    return f"projects/photos/{filename}"

def upload_to_news_photos(instance, filename):
    return f"news/photos/{filename}"

def upload_to_team_photos(instance, filename):
    return f"team/photos/{filename}"

def upload_to_service_icons(instance, filename):
    return f"services/icons/{filename}"

def upload_to_partner_logos(instance, filename):
    return f"partners/logos/{filename}"

def upload_to_work_process_images(instance, filename):
    return f"work_process/images/{filename}"


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
        ordering = ['order']
        indexes = [
            models.Index(fields=['about', 'order'], name='ix_about_logos_about_order'),
        ]
    
    def __str__(self):
        return f"About Logo {self.order}"


class PropertySector(TimestampMixin):
    """Property sectors model"""
    title = models.TextField(unique=True, help_text="Sector title")
    description = models.TextField(blank=True, null=True, help_text="Sector description")
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'property_sectors'
        verbose_name = 'Property Sector'
        verbose_name_plural = 'Property Sectors'
        ordering = ['order']
    
    def __str__(self):
        return self.title


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
    title = models.TextField(help_text="Project title")
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
    # Cover photo with file upload support
    cover_photo_file = models.ImageField(upload_to=upload_to_project_covers, blank=True, null=True, help_text="Upload cover photo")
    cover_photo_url = models.TextField(blank=True, null=True, help_text="Cover photo URL (auto-filled on file upload)")
    
    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-year', 'title']
    
    def save(self, *args, **kwargs):
        # If file is uploaded, generate URL
        if self.cover_photo_file:
            self.cover_photo_url = self.cover_photo_file.url
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class ProjectPhoto(TimestampMixin):
    """Project photos model"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='photos')
    # Photo with file upload support
    image_file = models.ImageField(upload_to=upload_to_project_photos, blank=True, null=True, help_text="Upload photo")
    image_url = models.TextField(blank=True, help_text="Photo URL (auto-filled on file upload)")
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'project_photos'
        verbose_name = 'Project Photo'
        verbose_name_plural = 'Project Photos'
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        # If file is uploaded, generate URL
        if self.image_file:
            self.image_url = self.image_file.url
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Photo {self.order} for {self.project.title}"


class News(TimestampMixin):
    """News articles model"""
    title = models.TextField(help_text="News title")
    summary = models.TextField(blank=True, null=True, help_text="News summary")
    # Photo with file upload support
    photo_file = models.ImageField(upload_to=upload_to_news_photos, blank=True, null=True, help_text="Upload news photo")
    photo_url = models.TextField(blank=True, null=True, help_text="News photo URL (auto-filled on file upload)")
    tags = ArrayField(models.TextField(), blank=True, default=list, help_text="News tags")
    
    class Meta:
        db_table = 'news'
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # If file is uploaded, generate URL
        if self.photo_file:
            self.photo_url = self.photo_file.url
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class NewsSection(TimestampMixin):
    """News sections model"""
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='sections')
    order = models.IntegerField(default=0, help_text="Section order")
    heading = models.TextField(blank=True, null=True, help_text="Section heading")
    content = models.TextField(blank=True, null=True, help_text="Section content")
    # Image with file upload support
    image_file = models.ImageField(upload_to=upload_to_news_photos, blank=True, null=True, help_text="Upload section image")
    image_url = models.TextField(blank=True, null=True, help_text="Section image URL (auto-filled on file upload)")
    
    class Meta:
        db_table = 'news_sections'
        verbose_name = 'News Section'
        verbose_name_plural = 'News Sections'
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        # If file is uploaded, generate URL
        if self.image_file:
            self.image_url = self.image_file.url
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Section {self.order} - {self.news.title}"


class TeamMember(TimestampMixin):
    """Team members model"""
    full_name = models.TextField(help_text="Team member full name")
    role = models.TextField(blank=True, null=True, help_text="Role/Position")
    # Photo with file upload support
    photo_file = models.ImageField(upload_to=upload_to_team_photos, blank=True, null=True, help_text="Upload member photo")
    photo_url = models.TextField(blank=True, null=True, help_text="Photo URL (auto-filled on file upload)")
    
    class Meta:
        db_table = 'team_members'
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
        ordering = ['full_name']
    
    def save(self, *args, **kwargs):
        # If file is uploaded, generate URL
        if self.photo_file:
            self.photo_url = self.photo_file.url
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.full_name


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
    title = models.TextField(help_text="Item title")
    description = models.TextField(blank=True, null=True, help_text="Item description")
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'team_section_items'
        verbose_name = 'Team Section Item'
        verbose_name_plural = 'Team Section Items'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.title} ({self.team_section.title})"


class Service(TimestampMixin):
    """Services model"""
    name = models.TextField(help_text="Service name")
    description = models.TextField(blank=True, null=True, help_text="Service description")
    order = models.IntegerField(default=0, help_text="Display order")
    # Icon with file upload support
    icon_file = models.ImageField(upload_to=upload_to_service_icons, blank=True, null=True, help_text="Upload service icon")
    icon_url = models.TextField(blank=True, null=True, help_text="Icon URL (auto-filled on file upload)")
    
    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        # If file is uploaded, generate URL
        if self.icon_file:
            self.icon_url = self.icon_file.url
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


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
    title = models.TextField(help_text="Approach title")
    description = models.TextField(blank=True, null=True, help_text="Approach description")
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'approaches'
        verbose_name = 'Approach'
        verbose_name_plural = 'Approaches'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Partner(TimestampMixin):
    """Partners model"""
    title = models.TextField(help_text="Partner title")
    button_text = models.TextField(blank=True, null=True, help_text="Button text")
    
    class Meta:
        db_table = 'partners'
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
    
    def __str__(self):
        return self.title


class PartnerLogo(TimestampMixin):
    """Partner logos model"""
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='logos')
    # Logo with file upload support
    image_file = models.ImageField(upload_to=upload_to_partner_logos, blank=True, null=True, help_text="Upload partner logo")
    image_url = models.TextField(blank=True, help_text="Logo image URL (auto-filled on file upload)")
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        db_table = 'partner_logos'
        verbose_name = 'Partner Logo'
        verbose_name_plural = 'Partner Logos'
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        # If file is uploaded, generate URL
        if self.image_file:
            self.image_url = self.image_file.url
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Logo {self.order} for {self.partner.title}"


class WorkProcess(TimestampMixin):
    """Work processes model"""
    title = models.TextField(help_text="Work process title")
    description = models.TextField(blank=True, null=True, help_text="Process description")
    order = models.IntegerField(default=0, help_text="Display order")
    # Image with file upload support
    image_file = models.ImageField(upload_to=upload_to_work_process_images, blank=True, null=True, help_text="Upload process image")
    image_url = models.TextField(blank=True, null=True, help_text="Process image URL (auto-filled on file upload)")
    
    class Meta:
        db_table = 'work_processes'
        verbose_name = 'Work Process'
        verbose_name_plural = 'Work Processes'
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        # If file is uploaded, generate URL
        if self.image_file:
            self.image_url = self.image_file.url
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
