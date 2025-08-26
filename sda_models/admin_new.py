from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms import Textarea
from .models import (
    About, AboutLogo, Service, ServiceBenefit, Approach, ContactMessage,
    News, NewsSection, Partner, PartnerLogo, PropertySector, SectorInn,
    Project, ProjectPhoto, TeamMember, TeamSection, TeamSectionItem, WorkProcess
)


# Custom admin configurations
class BaseAdmin(admin.ModelAdmin):
    """Base admin with common configurations"""
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 80})},
    }


# About models admin
class AboutLogoInline(admin.TabularInline):
    model = AboutLogo
    extra = 1
    fields = ('image_url', 'order')
    ordering = ('order',)


@admin.register(About)
class AboutAdmin(BaseAdmin):
    list_display = ('id', 'experience_preview', 'project_count', 'members', 'created_at')
    fields = ('experience', 'project_count', 'members', 'created_at', 'updated_at')
    inlines = [AboutLogoInline]
    
    def experience_preview(self, obj):
        return obj.experience[:100] + "..." if len(obj.experience) > 100 else obj.experience
    experience_preview.short_description = 'Experience'


@admin.register(AboutLogo)
class AboutLogoAdmin(BaseAdmin):
    list_display = ('id', 'about', 'image_preview', 'order', 'created_at')
    list_filter = ('about', 'created_at')
    ordering = ('about', 'order')
    fields = ('about', 'image_url', 'order', 'created_at', 'updated_at')
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Preview'


# Services admin
@admin.register(Service)
class ServiceAdmin(BaseAdmin):
    list_display = ('name', 'description_preview', 'order', 'created_at')
    list_editable = ('order',)
    ordering = ('order',)
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'icon_url', 'order', 'created_at', 'updated_at')
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
        return "-"
    description_preview.short_description = 'Description'


@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(BaseAdmin):
    list_display = ('title', 'description_preview', 'order', 'created_at')
    list_editable = ('order',)
    ordering = ('order',)
    search_fields = ('title', 'description')
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
        return "-"
    description_preview.short_description = 'Description'


# Approaches admin
@admin.register(Approach)
class ApproachAdmin(BaseAdmin):
    list_display = ('title', 'description_preview', 'order', 'created_at')
    list_editable = ('order',)
    ordering = ('order',)
    search_fields = ('title', 'description')
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
        return "-"
    description_preview.short_description = 'Description'


# Contact admin
@admin.register(ContactMessage)
class ContactMessageAdmin(BaseAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('first_name', 'last_name', 'email', 'phone_number', 'message', 'cv_url', 'created_at', 'updated_at')
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'


# News admin
class NewsSectionInline(admin.TabularInline):
    model = NewsSection
    extra = 1
    fields = ('order', 'heading', 'content', 'image_url')
    ordering = ('order',)


@admin.register(News)
class NewsAdmin(BaseAdmin):
    list_display = ('title', 'summary_preview', 'tags_display', 'created_at')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'summary', 'tags')
    fields = ('title', 'summary', 'photo_url', 'tags', 'created_at', 'updated_at')
    inlines = [NewsSectionInline]
    
    def summary_preview(self, obj):
        if obj.summary:
            return obj.summary[:100] + "..." if len(obj.summary) > 100 else obj.summary
        return "-"
    summary_preview.short_description = 'Summary'
    
    def tags_display(self, obj):
        return ", ".join(obj.tags) if obj.tags else "-"
    tags_display.short_description = 'Tags'


@admin.register(NewsSection)
class NewsSectionAdmin(BaseAdmin):
    list_display = ('news', 'heading', 'order', 'created_at')
    list_filter = ('news', 'created_at')
    ordering = ('news', 'order')


# Partners admin
class PartnerLogoInline(admin.TabularInline):
    model = PartnerLogo
    extra = 1
    fields = ('image_url', 'order')
    ordering = ('order',)


@admin.register(Partner)
class PartnerAdmin(BaseAdmin):
    list_display = ('title', 'button_text', 'logos_count', 'created_at')
    search_fields = ('title', 'button_text')
    inlines = [PartnerLogoInline]
    
    def logos_count(self, obj):
        return obj.logos.count()
    logos_count.short_description = 'Logos Count'


@admin.register(PartnerLogo)
class PartnerLogoAdmin(BaseAdmin):
    list_display = ('partner', 'image_preview', 'order', 'created_at')
    list_filter = ('partner', 'created_at')
    ordering = ('partner', 'order')
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Preview'


# Property Sectors admin
class SectorInnInline(admin.TabularInline):
    model = SectorInn
    extra = 1
    fields = ('title', 'description', 'order')
    ordering = ('order',)


@admin.register(PropertySector)
class PropertySectorAdmin(BaseAdmin):
    list_display = ('title', 'description_preview', 'order', 'inns_count', 'projects_count', 'created_at')
    list_editable = ('order',)
    ordering = ('order',)
    search_fields = ('title', 'description')
    inlines = [SectorInnInline]
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
        return "-"
    description_preview.short_description = 'Description'
    
    def inns_count(self, obj):
        return obj.inns.count()
    inns_count.short_description = 'Inns Count'
    
    def projects_count(self, obj):
        return obj.projects.count()
    projects_count.short_description = 'Projects Count'


@admin.register(SectorInn)
class SectorInnAdmin(BaseAdmin):
    list_display = ('title', 'property_sector', 'description_preview', 'order', 'created_at')
    list_filter = ('property_sector', 'created_at')
    ordering = ('property_sector', 'order')
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
        return "-"
    description_preview.short_description = 'Description'


# Projects admin
class ProjectPhotoInline(admin.TabularInline):
    model = ProjectPhoto
    extra = 1
    fields = ('image_url', 'order')
    ordering = ('order',)


@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    list_display = ('title', 'client', 'year', 'property_sector', 'tag', 'photos_count', 'created_at')
    list_filter = ('year', 'property_sector', 'tag', 'created_at')
    search_fields = ('title', 'client', 'tag')
    fields = ('title', 'client', 'year', 'property_sector', 'tag', 'cover_photo_url', 'created_at', 'updated_at')
    inlines = [ProjectPhotoInline]
    
    def photos_count(self, obj):
        return obj.photos.count()
    photos_count.short_description = 'Photos Count'


@admin.register(ProjectPhoto)
class ProjectPhotoAdmin(BaseAdmin):
    list_display = ('project', 'image_preview', 'order', 'created_at')
    list_filter = ('project', 'created_at')
    ordering = ('project', 'order')
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Preview'


# Team admin
@admin.register(TeamMember)
class TeamMemberAdmin(BaseAdmin):
    list_display = ('full_name', 'role', 'photo_preview', 'created_at')
    search_fields = ('full_name', 'role')
    fields = ('full_name', 'role', 'photo_url', 'created_at', 'updated_at')
    
    def photo_preview(self, obj):
        if obj.photo_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 50%;" />', obj.photo_url)
        return "No photo"
    photo_preview.short_description = 'Photo'


class TeamSectionItemInline(admin.TabularInline):
    model = TeamSectionItem
    extra = 1
    fields = ('name', 'description', 'photo_url', 'button_text', 'order')
    ordering = ('order',)


@admin.register(TeamSection)
class TeamSectionAdmin(BaseAdmin):
    list_display = ('title', 'button_text', 'items_count', 'created_at')
    search_fields = ('title', 'button_text')
    inlines = [TeamSectionItemInline]
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items Count'


@admin.register(TeamSectionItem)
class TeamSectionItemAdmin(BaseAdmin):
    list_display = ('name', 'team_section', 'description_preview', 'order', 'created_at')
    list_filter = ('team_section', 'created_at')
    ordering = ('team_section', 'order')
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
        return "-"
    description_preview.short_description = 'Description'


# Work Process admin
@admin.register(WorkProcess)
class WorkProcessAdmin(BaseAdmin):
    list_display = ('title', 'description_preview', 'order', 'image_preview', 'created_at')
    list_editable = ('order',)
    ordering = ('order',)
    search_fields = ('title', 'description')
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
        return "-"
    description_preview.short_description = 'Description'
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Image'


# Admin site customization
admin.site.site_header = "SDA Administration Panel"
admin.site.site_title = "SDA Admin"
admin.site.index_title = "Welcome to SDA Content Management"
