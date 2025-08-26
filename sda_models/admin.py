from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models_fixed import (
    PropertySector, Project, ProjectPhoto, Partner, PartnerLogo,
    About, AboutLogo, Service, ServiceBenefit, News, TeamMember,
    TeamSection, TeamSectionItem, WorkProcess, Approach, Contact
)


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
        if hasattr(obj, 'image') and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.image.url
            )
        elif hasattr(obj, 'photo') and obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.photo.url
            )
        elif hasattr(obj, 'icon') and obj.icon:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.icon.url
            )
        elif hasattr(obj, 'cover_photo') and obj.cover_photo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.cover_photo.url
            )
        return "No image"
    
    image_preview.short_description = "Preview"


# Inline classes
class ProjectPhotoInline(admin.TabularInline):
    model = ProjectPhoto
    extra = 1
    fields = ('image', 'image_url', 'order')
    readonly_fields = ('image_url',)


class PartnerLogoInline(admin.TabularInline):
    model = PartnerLogo
    extra = 1
    fields = ('image', 'image_url', 'order')
    readonly_fields = ('image_url',)


class AboutLogoInline(admin.TabularInline):
    model = AboutLogo
    extra = 1
    fields = ('image', 'image_url', 'order')
    readonly_fields = ('image_url',)


class ServiceBenefitInline(admin.TabularInline):
    model = ServiceBenefit
    extra = 1
    fields = ('title', 'description', 'order')


class TeamSectionItemInline(admin.TabularInline):
    model = TeamSectionItem
    extra = 1
    fields = ('name', 'position', 'photo', 'photo_url', 'display_order')
    readonly_fields = ('photo_url',)


# Main admin classes
@admin.register(PropertySector)
class PropertySectorAdmin(BaseAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)


@admin.register(Project)
class ProjectAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('title', 'tag', 'client', 'year', 'property_sector', 'image_preview', 'created_at')
    list_filter = ('property_sector', 'year', 'tag', 'created_at')
    search_fields = ('title', 'client', 'tag')
    fields = (
        'title', 'tag', 'client', 'year', 'property_sector',
        'cover_photo', 'cover_photo_url',
        'created_at', 'updated_at'
    )
    readonly_fields = ('cover_photo_url', 'created_at', 'updated_at')
    inlines = [ProjectPhotoInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('property_sector')


@admin.register(ProjectPhoto)
class ProjectPhotoAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('project', 'image_preview', 'order', 'created_at')
    list_filter = ('project', 'created_at')
    search_fields = ('project__title',)
    fields = ('project', 'image', 'image_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('image_url', 'created_at', 'updated_at')


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
    list_display = ('partner', 'image_preview', 'order', 'created_at')
    list_filter = ('partner', 'created_at')
    search_fields = ('partner__title',)
    fields = ('partner', 'image', 'image_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('image_url', 'created_at', 'updated_at')


@admin.register(About)
class AboutAdmin(BaseAdmin):
    list_display = ('experience', 'project_count', 'members', 'created_at')
    search_fields = ('experience', 'description')
    list_filter = ('created_at',)
    fields = ('experience', 'project_count', 'members', 'description', 'created_at', 'updated_at')
    inlines = [AboutLogoInline]


@admin.register(AboutLogo)
class AboutLogoAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('about', 'image_preview', 'order', 'created_at')
    list_filter = ('about', 'created_at')
    fields = ('about', 'image', 'image_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('image_url', 'created_at', 'updated_at')


@admin.register(Service)
class ServiceAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('title', 'image_preview', 'order', 'benefit_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'icon', 'icon_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('icon_url', 'created_at', 'updated_at')
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
    list_display = ('title', 'image_preview', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'image', 'image_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('image_url', 'created_at', 'updated_at')


@admin.register(TeamMember)
class TeamMemberAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('full_name', 'role', 'image_preview', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('full_name', 'role')
    fields = ('full_name', 'role', 'photo', 'photo_url', 'created_at', 'updated_at')
    readonly_fields = ('photo_url', 'created_at', 'updated_at')


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
    list_display = ('name', 'team_section', 'position', 'department', 'image_preview', 'display_order', 'created_at')
    list_filter = ('team_section', 'position', 'department', 'created_at')
    search_fields = ('name', 'position', 'department', 'bio')
    fields = (
        'team_section', 'name', 'position', 'department', 'bio',
        'photo', 'photo_url', 'display_order',
        'created_at', 'updated_at'
    )
    readonly_fields = ('photo_url', 'created_at', 'updated_at')


@admin.register(WorkProcess)
class WorkProcessAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('title', 'image_preview', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'image', 'photo_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('photo_url', 'created_at', 'updated_at')


@admin.register(Approach)
class ApproachAdmin(BaseAdmin):
    list_display = ('title', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'order', 'created_at', 'updated_at')


@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    list_display = ('email', 'phone', 'created_at')
    search_fields = ('email', 'phone', 'address')
    fields = (
        'address', 'phone', 'email',
        'linkedin', 'instagram', 'youtube',
        'created_at', 'updated_at'
    )

    def has_add_permission(self, request):
        # Only allow one contact record
        return not Contact.objects.exists()


# Customize admin site
admin.site.site_header = "SDA Admin Panel"
admin.site.site_title = "SDA Admin"
admin.site.index_title = "Welcome to SDA Administration"
