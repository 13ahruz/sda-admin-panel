from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    PropertySector, SectorInn, Project, ProjectPhoto, Partner, PartnerLogo,
    About, AboutLogo, Service, ServiceBenefit, News, TeamMember,
    TeamSection, TeamSectionItem, WorkProcess, Approach, ContactMessage
)
from .forms import (
    ProjectPhotoAdminForm, PartnerLogoAdminForm, 
    AboutLogoAdminForm, ServiceAdminForm, NewsAdminForm, 
    TeamMemberAdminForm, TeamSectionItemAdminForm, WorkProcessAdminForm
)
from .simple_forms import ProjectSimpleAdminForm


class BaseAdmin(admin.ModelAdmin):
    """Base admin with common functionality"""
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('created_at', 'updated_at')
        return self.readonly_fields


class ImagePreviewMixin:
    """Mixin to add image preview functionality"""
    
    def image_preview(self, obj):
        image_url = None
        
        # Check for various URL fields
        if hasattr(obj, 'image_url') and obj.image_url:
            image_url = obj.image_url
        elif hasattr(obj, 'photo_url') and obj.photo_url:
            image_url = obj.photo_url
        elif hasattr(obj, 'cover_photo_url') and obj.cover_photo_url:
            image_url = obj.cover_photo_url
        elif hasattr(obj, 'icon_url') and obj.icon_url:
            image_url = obj.icon_url
        
        if image_url:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                image_url
            )
        return "No image"
    
    image_preview.short_description = "Preview"
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('created_at', 'updated_at')
        return self.readonly_fields


class ImagePreviewMixin:
    """Mixin to add image preview functionality"""
    
    def image_preview(self, obj):
        image_url = None
        
        # Check for various URL fields
        if hasattr(obj, 'image_url') and obj.image_url:
            image_url = obj.image_url
        elif hasattr(obj, 'photo_url') and obj.photo_url:
            image_url = obj.photo_url
        elif hasattr(obj, 'cover_photo_url') and obj.cover_photo_url:
            image_url = obj.cover_photo_url
        
        if image_url:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                image_url
            )
        return "No image"
    
    image_preview.short_description = "Preview"


# Inline classes
class ProjectPhotoInline(admin.TabularInline):
    model = ProjectPhoto
    extra = 1
    fields = ('image_url', 'order')


class PartnerLogoInline(admin.TabularInline):
    model = PartnerLogo
    extra = 1
    fields = ('image_url', 'order')


class AboutLogoInline(admin.TabularInline):
    model = AboutLogo
    extra = 1
    fields = ('image_url', 'order')


class ServiceBenefitInline(admin.TabularInline):
    model = ServiceBenefit
    extra = 1
    fields = ('title', 'description', 'order')


class SectorInnInline(admin.TabularInline):
    model = SectorInn
    extra = 1
    fields = ('title', 'description', 'order')


class TeamSectionItemInline(admin.TabularInline):
    model = TeamSectionItem
    extra = 1
    fields = ('name', 'position', 'photo_url', 'display_order')
    readonly_fields = ()


# Main admin classes
@admin.register(PropertySector)
class PropertySectorAdmin(BaseAdmin):
    list_display = ('title', 'description', 'order', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    fields = ('title', 'description', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SectorInnInline]


@admin.register(SectorInn)
class SectorInnAdmin(BaseAdmin):
    list_display = ('property_sector', 'title', 'order', 'created_at')
    list_filter = ('property_sector', 'created_at')
    search_fields = ('title', 'description', 'property_sector__title')
    fields = ('property_sector', 'title', 'description', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Project)
class ProjectAdmin(BaseAdmin, ImagePreviewMixin):
    form = ProjectSimpleAdminForm
    list_display = ('title', 'tag', 'client', 'year', 'property_sector', 'image_preview', 'created_at')
    list_filter = ('property_sector', 'year', 'tag', 'created_at')
    search_fields = ('title', 'client', 'tag')
    fields = (
        'title', 'tag', 'client', 'year', 'property_sector',
        'cover_photo_url',
        'created_at', 'updated_at'
    )
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProjectPhotoInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('property_sector')


@admin.register(ProjectPhoto)
class ProjectPhotoAdmin(BaseAdmin, ImagePreviewMixin):
    form = ProjectPhotoAdminForm
    list_display = ('project', 'image_preview', 'order', 'created_at')
    list_filter = ('project', 'created_at')
    search_fields = ('project__title',)
    fields = ('project', 'image_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Partner)
class PartnerAdmin(BaseAdmin):
    list_display = ('title', 'button_text', 'logo_count', 'created_at')
    search_fields = ('title', 'button_text')
    list_filter = ('created_at',)
    inlines = [PartnerLogoInline]

    def logo_count(self, obj):
        return obj.logos.count()
    logo_count.short_description = 'Logos'


@admin.register(PartnerLogo)
class PartnerLogoAdmin(BaseAdmin, ImagePreviewMixin):
    form = PartnerLogoAdminForm
    list_display = ('partner', 'image_preview', 'order', 'created_at')
    list_filter = ('partner', 'created_at')
    search_fields = ('partner__title',)
    fields = ('partner', 'image_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(About)
class AboutAdmin(BaseAdmin):
    list_display = ('experience', 'project_count', 'members', 'created_at')
    search_fields = ('experience', 'description')
    list_filter = ('created_at',)
    fields = ('experience', 'project_count', 'members', 'description', 'created_at', 'updated_at')
    inlines = [AboutLogoInline]


@admin.register(AboutLogo)
class AboutLogoAdmin(BaseAdmin, ImagePreviewMixin):
    form = AboutLogoAdminForm
    list_display = ('about', 'image_preview', 'order', 'created_at')
    list_filter = ('about', 'created_at')
    fields = ('about', 'image_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Service)
class ServiceAdmin(BaseAdmin, ImagePreviewMixin):
    form = ServiceAdminForm
    list_display = ('title', 'image_preview', 'order', 'benefit_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'icon_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ServiceBenefitInline]

    def benefit_count(self, obj):
        return obj.benefits.count()
    benefit_count.short_description = 'Benefits'


@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(BaseAdmin):
    list_display = ('service', 'title', 'order', 'created_at')
    list_filter = ('service', 'created_at')
    search_fields = ('title', 'description', 'service__title')
    fields = ('service', 'title', 'description', 'order', 'created_at', 'updated_at')


@admin.register(News)
class NewsAdmin(BaseAdmin, ImagePreviewMixin):
    form = NewsAdminForm
    list_display = ('title', 'image_preview', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'image_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TeamMember)
class TeamMemberAdmin(BaseAdmin, ImagePreviewMixin):
    form = TeamMemberAdminForm
    list_display = ('full_name', 'role', 'image_preview', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('full_name', 'role')
    fields = ('full_name', 'role', 'photo_url', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TeamSection)
class TeamSectionAdmin(BaseAdmin):
    list_display = ('title', 'order', 'item_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'order', 'created_at', 'updated_at')
    inlines = [TeamSectionItemInline]

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(TeamSectionItem)
class TeamSectionItemAdmin(BaseAdmin, ImagePreviewMixin):
    form = TeamSectionItemAdminForm
    list_display = ('name', 'team_section', 'position', 'department', 'image_preview', 'display_order', 'created_at')
    list_filter = ('team_section', 'position', 'department', 'created_at')
    search_fields = ('name', 'position', 'department', 'bio')
    fields = (
        'team_section', 'name', 'position', 'department', 'bio',
        'photo_url', 'display_order',
        'created_at', 'updated_at'
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(WorkProcess)
class WorkProcessAdmin(BaseAdmin, ImagePreviewMixin):
    form = WorkProcessAdminForm
    list_display = ('title', 'image_preview', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'image_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Approach)
class ApproachAdmin(BaseAdmin):
    list_display = ('title', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'order', 'created_at', 'updated_at')


@admin.register(ContactMessage)
class ContactMessageAdmin(BaseAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'message')
    list_filter = ('created_at',)
    fields = (
        'first_name', 'last_name', 'phone_number', 'email', 'message', 'cv_url',
        'created_at', 'updated_at'
    )
    readonly_fields = ('created_at', 'updated_at')


# Customize admin site
admin.site.site_header = "SDA Admin Panel"
admin.site.site_title = "SDA Admin"
admin.site.index_title = "Welcome to SDA Administration"
