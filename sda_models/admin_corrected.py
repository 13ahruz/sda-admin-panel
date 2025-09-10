from django.contrib import admin
from django.utils.html import format_html
from .models import *


class BaseAdmin(admin.ModelAdmin):
    """Base admin class with common configurations"""
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    

class ImagePreviewMixin:
    """Mixin for admin classes that need image preview functionality"""
    def image_preview(self, obj):
        if hasattr(obj, 'photo_url') and obj.photo_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.photo_url)
        elif hasattr(obj, 'cover_photo_url') and obj.cover_photo_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.cover_photo_url)
        elif hasattr(obj, 'icon_url') and obj.icon_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.icon_url)
        elif hasattr(obj, 'image_url') and obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Preview'


# Inline classes
class AboutLogoInline(admin.TabularInline):
    model = AboutLogo
    extra = 1
    fields = ('image_url', 'order')


class SectorInnInline(admin.TabularInline):
    model = SectorInn
    extra = 1
    fields = ('title', 'description', 'order')


class ProjectPhotoInline(admin.TabularInline):
    model = ProjectPhoto
    extra = 1
    fields = ('image_url', 'order')


class PartnerLogoInline(admin.TabularInline):
    model = PartnerLogo
    extra = 1
    fields = ('image_url', 'order')


class NewsSectionInline(admin.TabularInline):
    model = NewsSection
    extra = 1
    fields = ('heading', 'content', 'image_url', 'order')


class TeamSectionItemInline(admin.TabularInline):
    model = TeamSectionItem
    extra = 1
    fields = ('title', 'description', 'order')


# Main admin classes
@admin.register(About)
class AboutAdmin(BaseAdmin):
    list_display = ('experience', 'project_count', 'members', 'created_at')
    search_fields = ('experience', 'project_count', 'members')
    list_filter = ('created_at',)
    fields = ('experience', 'project_count', 'members', 'created_at', 'updated_at')
    inlines = [AboutLogoInline]


@admin.register(PropertySector)
class PropertySectorAdmin(BaseAdmin):
    list_display = ('title', 'description', 'order', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    fields = ('title', 'description', 'order', 'created_at', 'updated_at')
    ordering = ['order']
    inlines = [SectorInnInline]


@admin.register(SectorInn)
class SectorInnAdmin(BaseAdmin):
    list_display = ('title', 'property_sector', 'description', 'order', 'created_at')
    list_filter = ('property_sector', 'created_at')
    search_fields = ('title', 'description', 'property_sector__title')
    fields = ('property_sector', 'title', 'description', 'order', 'created_at', 'updated_at')


@admin.register(Project)
class ProjectAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('title', 'client', 'year', 'property_sector', 'image_preview', 'created_at')
    list_filter = ('year', 'property_sector', 'created_at')
    search_fields = ('title', 'client', 'tag')
    fields = ('title', 'tag', 'client', 'year', 'property_sector', 'cover_photo_url', 'created_at', 'updated_at')
    inlines = [ProjectPhotoInline]


@admin.register(ProjectPhoto)
class ProjectPhotoAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('project', 'image_preview', 'order', 'created_at')
    list_filter = ('project', 'created_at')
    search_fields = ('project__title',)
    fields = ('project', 'image_url', 'order', 'created_at', 'updated_at')


@admin.register(News)
class NewsAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('title', 'image_preview', 'created_at')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'summary', 'tags')
    fields = ('title', 'summary', 'photo_url', 'tags', 'created_at', 'updated_at')
    inlines = [NewsSectionInline]


@admin.register(NewsSection)
class NewsSectionAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('news', 'heading', 'order', 'image_preview', 'created_at')
    list_filter = ('news', 'created_at')
    search_fields = ('heading', 'content', 'news__title')
    fields = ('news', 'heading', 'content', 'image_url', 'order', 'created_at', 'updated_at')


@admin.register(TeamMember)
class TeamMemberAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('full_name', 'role', 'image_preview', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('full_name', 'role')
    fields = ('full_name', 'role', 'photo_url', 'created_at', 'updated_at')


@admin.register(TeamSection)
class TeamSectionAdmin(BaseAdmin):
    list_display = ('title', 'button_text', 'created_at')
    search_fields = ('title', 'button_text')
    list_filter = ('created_at',)
    fields = ('title', 'button_text', 'created_at', 'updated_at')
    inlines = [TeamSectionItemInline]


@admin.register(TeamSectionItem)
class TeamSectionItemAdmin(BaseAdmin):
    list_display = ('title', 'team_section', 'description', 'order', 'created_at')
    list_filter = ('team_section', 'created_at')
    search_fields = ('title', 'description', 'team_section__title')
    fields = ('team_section', 'title', 'description', 'order', 'created_at', 'updated_at')


@admin.register(Service)
class ServiceAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('name', 'description', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'order', 'icon_url', 'created_at', 'updated_at')
    ordering = ['order']


@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(BaseAdmin):
    list_display = ('title', 'description', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'order', 'created_at', 'updated_at')


@admin.register(ContactMessage)
class ContactMessageAdmin(BaseAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'message')
    list_filter = ('created_at',)
    fields = ('first_name', 'last_name', 'phone_number', 'email', 'message', 'cv_url', 'created_at', 'updated_at')


@admin.register(Approach)
class ApproachAdmin(BaseAdmin):
    list_display = ('title', 'description', 'order', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    fields = ('title', 'description', 'order', 'created_at', 'updated_at')
    ordering = ['order']


@admin.register(Partner)
class PartnerAdmin(BaseAdmin):
    list_display = ('title', 'button_text', 'created_at')
    search_fields = ('title', 'button_text')
    list_filter = ('created_at',)
    fields = ('title', 'button_text', 'created_at', 'updated_at')
    inlines = [PartnerLogoInline]


@admin.register(PartnerLogo)
class PartnerLogoAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('partner', 'image_preview', 'order', 'created_at')
    list_filter = ('partner', 'created_at')
    search_fields = ('partner__title',)
    fields = ('partner', 'image_url', 'order', 'created_at', 'updated_at')


@admin.register(WorkProcess)
class WorkProcessAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('title', 'description', 'order', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    fields = ('title', 'description', 'order', 'image_url', 'created_at', 'updated_at')
    ordering = ['order']


# Customize admin site
admin.site.site_header = "SDA Admin Panel"
admin.site.site_title = "SDA Admin"
admin.site.index_title = "Welcome to SDA Administration"
