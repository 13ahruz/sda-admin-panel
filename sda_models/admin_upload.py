from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models_upload import (
    About, AboutLogo, Service, Partner, Project, ProjectImage,
    News, Team, PropertySector, Approach, WorkProcess, Contact
)


class BaseAdmin(admin.ModelAdmin):
    """Base admin class with common functionality"""
    list_per_page = 20
    save_on_top = True
    
    def get_readonly_fields(self, request, obj=None):
        """Make timestamp fields readonly"""
        readonly = list(super().get_readonly_fields(request, obj))
        readonly.extend(['created_at', 'updated_at'])
        return readonly


class AboutLogoInline(admin.TabularInline):
    """Inline admin for About logos"""
    model = AboutLogo
    extra = 1
    fields = ['image_file', 'image_url', 'order', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image_url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(About)
class AboutAdmin(BaseAdmin):
    """Admin for About model"""
    inlines = [AboutLogoInline]
    list_display = ['id', 'experience', 'project_count', 'members', 'created_at']
    search_fields = ['experience', 'project_count', 'members']
    fieldsets = (
        ('About Information', {
            'fields': ['experience', 'project_count', 'members']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    )


@admin.register(Service)
class ServiceAdmin(BaseAdmin):
    """Admin for Service model"""
    list_display = ['title', 'description_short', 'image_preview', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['created_at']
    fieldsets = (
        ('Service Information', {
            'fields': ['title', 'description']
        }),
        ('Image', {
            'fields': ['image_file', 'image_url', 'image_preview']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    )
    readonly_fields = ['image_preview']
    
    def description_short(self, obj):
        return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
    description_short.short_description = "Description"
    
    def image_preview(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image_url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(Partner)
class PartnerAdmin(BaseAdmin):
    """Admin for Partner model"""
    list_display = ['name', 'website_url', 'logo_preview', 'order', 'created_at']
    search_fields = ['name', 'website_url']
    list_filter = ['created_at']
    list_editable = ['order']
    ordering = ['order']
    fieldsets = (
        ('Partner Information', {
            'fields': ['name', 'website_url', 'order']
        }),
        ('Logo', {
            'fields': ['logo_file', 'logo_url', 'logo_preview']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    )
    readonly_fields = ['logo_preview']
    
    def logo_preview(self, obj):
        if obj.logo_file:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.logo_file.url)
        elif obj.logo_url:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.logo_url)
        return "No logo"
    logo_preview.short_description = "Logo Preview"


class ProjectImageInline(admin.TabularInline):
    """Inline admin for Project images"""
    model = ProjectImage
    extra = 1
    fields = ['image_file', 'image_url', 'order', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image_url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    """Admin for Project model"""
    inlines = [ProjectImageInline]
    list_display = ['title', 'location', 'year', 'category', 'cover_preview', 'created_at']
    search_fields = ['title', 'description', 'location', 'category']
    list_filter = ['year', 'category', 'created_at']
    fieldsets = (
        ('Project Information', {
            'fields': ['title', 'description', 'location', 'year', 'category']
        }),
        ('Cover Image', {
            'fields': ['cover_image_file', 'cover_image_url', 'cover_preview']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    )
    readonly_fields = ['cover_preview']
    
    def cover_preview(self, obj):
        if obj.cover_image_file:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.cover_image_file.url)
        elif obj.cover_image_url:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.cover_image_url)
        return "No cover image"
    cover_preview.short_description = "Cover Preview"


@admin.register(News)
class NewsAdmin(BaseAdmin):
    """Admin for News model"""
    list_display = ['title', 'summary_short', 'is_published', 'image_preview', 'created_at']
    search_fields = ['title', 'content', 'summary']
    list_filter = ['is_published', 'created_at']
    list_editable = ['is_published']
    fieldsets = (
        ('Article Information', {
            'fields': ['title', 'summary', 'content', 'is_published']
        }),
        ('Image', {
            'fields': ['image_file', 'image_url', 'image_preview']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    )
    readonly_fields = ['image_preview']
    
    def summary_short(self, obj):
        if obj.summary:
            return obj.summary[:100] + "..." if len(obj.summary) > 100 else obj.summary
        return "No summary"
    summary_short.short_description = "Summary"
    
    def image_preview(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image_url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(Team)
class TeamAdmin(BaseAdmin):
    """Admin for Team model"""
    list_display = ['name', 'position', 'email', 'phone', 'photo_preview', 'order']
    search_fields = ['name', 'position', 'email', 'bio']
    list_filter = ['position', 'created_at']
    list_editable = ['order']
    ordering = ['order']
    fieldsets = (
        ('Personal Information', {
            'fields': ['name', 'position', 'bio', 'order']
        }),
        ('Contact Information', {
            'fields': ['email', 'phone']
        }),
        ('Photo', {
            'fields': ['photo_file', 'photo_url', 'photo_preview']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    )
    readonly_fields = ['photo_preview']
    
    def photo_preview(self, obj):
        if obj.photo_file:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.photo_file.url)
        elif obj.photo_url:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.photo_url)
        return "No photo"
    photo_preview.short_description = "Photo Preview"


@admin.register(PropertySector)
class PropertySectorAdmin(BaseAdmin):
    """Admin for Property Sector model"""
    list_display = ['title', 'description_short', 'order', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order']
    ordering = ['order']
    
    def description_short(self, obj):
        return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
    description_short.short_description = "Description"


@admin.register(Approach)
class ApproachAdmin(BaseAdmin):
    """Admin for Approach model"""
    list_display = ['title', 'description_short', 'order', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order']
    ordering = ['order']
    
    def description_short(self, obj):
        return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
    description_short.short_description = "Description"


@admin.register(WorkProcess)
class WorkProcessAdmin(BaseAdmin):
    """Admin for Work Process model"""
    list_display = ['step_number', 'title', 'description_short', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['step_number', 'created_at']
    ordering = ['step_number']
    
    def description_short(self, obj):
        return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
    description_short.short_description = "Description"


@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    """Admin for Contact model"""
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at', 'updated_at']
    
    def has_add_permission(self, request):
        return False  # Prevent adding contact submissions through admin
    
    def has_delete_permission(self, request, obj=None):
        return True  # Allow deleting contact submissions


# Customize admin site
admin.site.site_header = "SDA Admin Panel"
admin.site.site_title = "SDA Admin"
admin.site.index_title = "Welcome to SDA Administration"
