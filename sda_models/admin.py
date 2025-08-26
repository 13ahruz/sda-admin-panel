from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (
    About, AboutLogo, PropertySector, SectorInn, Project, ProjectPhoto,
    News, NewsSection, TeamMember, TeamSection, TeamSectionItem,
    Service, ServiceBenefit, ContactMessage, Approach, Partner, 
    PartnerLogo, WorkProcess
)


# Resources for import/export functionality
class AboutResource(resources.ModelResource):
    class Meta:
        model = About


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project


class NewsResource(resources.ModelResource):
    class Meta:
        model = News


class ContactMessageResource(resources.ModelResource):
    class Meta:
        model = ContactMessage


class ApproachResource(resources.ModelResource):
    class Meta:
        model = Approach


class PartnerResource(resources.ModelResource):
    class Meta:
        model = Partner


class WorkProcessResource(resources.ModelResource):
    class Meta:
        model = WorkProcess


# Inline admin classes
class AboutLogoInline(admin.TabularInline):
    model = AboutLogo
    extra = 1
    fields = ('image_file', 'image_url', 'order')
    readonly_fields = ('image_url',)
    ordering = ['order']


class SectorInnInline(admin.TabularInline):
    model = SectorInn
    extra = 1
    fields = ('title', 'description', 'order')
    ordering = ['order']


class ProjectPhotoInline(admin.TabularInline):
    model = ProjectPhoto
    extra = 1
    fields = ('image_file', 'image_url', 'order')
    readonly_fields = ('image_url',)
    ordering = ['order']


class NewsSectionInline(admin.StackedInline):
    model = NewsSection
    extra = 1
    fields = ('order', 'heading', 'content', 'image_file', 'image_url')
    readonly_fields = ('image_url',)
    ordering = ['order']


class TeamSectionItemInline(admin.TabularInline):
    model = TeamSectionItem
    extra = 1
    fields = ('title', 'description', 'order')
    ordering = ['order']


class PartnerLogoInline(admin.TabularInline):
    model = PartnerLogo
    extra = 1
    fields = ('image_file', 'image_url', 'order')
    readonly_fields = ('image_url',)
    ordering = ['order']


# Main admin classes
@admin.register(About)
class AboutAdmin(ImportExportModelAdmin):
    resource_class = AboutResource
    list_display = ['id', 'experience_preview', 'project_count', 'members_preview', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['experience', 'project_count', 'members']
    inlines = [AboutLogoInline]
    readonly_fields = ['created_at', 'updated_at']
    
    def experience_preview(self, obj):
        return obj.experience[:50] + '...' if len(obj.experience) > 50 else obj.experience
    experience_preview.short_description = 'Experience'
    
    def members_preview(self, obj):
        return obj.members[:50] + '...' if len(obj.members) > 50 else obj.members
    members_preview.short_description = 'Members'


@admin.register(AboutLogo)
class AboutLogoAdmin(admin.ModelAdmin):
    list_display = ['id', 'about', 'image_preview', 'order', 'created_at']
    list_filter = ['about', 'created_at']
    list_editable = ['order']
    fields = ('about', 'image_file', 'image_url', 'order')
    readonly_fields = ('image_url',)
    ordering = ['about', 'order']
    
    def image_preview(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Image Preview'


@admin.register(PropertySector)
class PropertySectorAdmin(admin.ModelAdmin):
    list_display = ['title', 'description_preview', 'order', 'project_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description']
    list_editable = ['order']
    inlines = [SectorInnInline]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order']
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "No description"
    description_preview.short_description = 'Description'
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'


@admin.register(SectorInn)
class SectorInnAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_sector', 'description_preview', 'order', 'created_at']
    list_filter = ['property_sector', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order']
    ordering = ['property_sector', 'order']
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "No description"
    description_preview.short_description = 'Description'


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource
    list_display = ['title', 'property_sector', 'client', 'year', 'tag', 'cover_preview', 'photo_count', 'created_at']
    list_filter = ['property_sector', 'year', 'created_at']
    search_fields = ['title', 'client', 'tag']
    fields = ('title', 'property_sector', 'client', 'year', 'tag', 'cover_photo_file', 'cover_photo_url')
    readonly_fields = ('cover_photo_url', 'created_at', 'updated_at')
    inlines = [ProjectPhotoInline]
    ordering = ['-year', 'title']
    
    def cover_preview(self, obj):
        if obj.cover_photo_file:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.cover_photo_file.url)
        elif obj.cover_photo_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.cover_photo_url)
        return "No cover"
    cover_preview.short_description = 'Cover'
    
    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Photos'


@admin.register(ProjectPhoto)
class ProjectPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'image_preview', 'order', 'created_at']
    list_filter = ['project', 'created_at']
    list_editable = ['order']
    fields = ('project', 'image_file', 'image_url', 'order')
    readonly_fields = ('image_url',)
    ordering = ['project', 'order']
    
    def image_preview(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Image Preview'


@admin.register(News)
class NewsAdmin(ImportExportModelAdmin):
    resource_class = NewsResource
    list_display = ['title', 'summary_preview', 'tags_display', 'photo_preview', 'section_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'summary', 'tags']
    inlines = [NewsSectionInline]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def summary_preview(self, obj):
        if obj.summary:
            return obj.summary[:50] + '...' if len(obj.summary) > 50 else obj.summary
        return "No summary"
    summary_preview.short_description = 'Summary'
    
    def tags_display(self, obj):
        return ', '.join(obj.tags) if obj.tags else "No tags"
    tags_display.short_description = 'Tags'
    
    def photo_preview(self, obj):
        if obj.photo_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.photo_url)
        return "No photo"
    photo_preview.short_description = 'Photo'
    
    def section_count(self, obj):
        return obj.sections.count()
    section_count.short_description = 'Sections'


@admin.register(NewsSection)
class NewsSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'news', 'heading', 'content_preview', 'image_preview', 'order', 'created_at']
    list_filter = ['news', 'created_at']
    search_fields = ['heading', 'content']
    list_editable = ['order']
    ordering = ['news', 'order']
    
    def content_preview(self, obj):
        if obj.content:
            return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
        return "No content"
    content_preview.short_description = 'Content'
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Image'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'role', 'photo_preview', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['full_name', 'role']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['full_name']
    
    def photo_preview(self, obj):
        if obj.photo_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.photo_url)
        return "No photo"
    photo_preview.short_description = 'Photo'


@admin.register(TeamSection)
class TeamSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'button_text', 'item_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'button_text']
    inlines = [TeamSectionItemInline]
    readonly_fields = ['created_at', 'updated_at']
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(TeamSectionItem)
class TeamSectionItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'team_section', 'description_preview', 'order', 'created_at']
    list_filter = ['team_section', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order']
    ordering = ['team_section', 'order']
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "No description"
    description_preview.short_description = 'Description'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description_preview', 'order', 'icon_preview', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_editable = ['order']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order']
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "No description"
    description_preview.short_description = 'Description'
    
    def icon_preview(self, obj):
        if obj.icon_url:
            return format_html('<img src="{}" style="max-height: 30px; max-width: 30px;" />', obj.icon_url)
        return "No icon"
    icon_preview.short_description = 'Icon'


@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(admin.ModelAdmin):
    list_display = ['title', 'description_preview', 'order', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description']
    list_editable = ['order']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order']
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "No description"
    description_preview.short_description = 'Description'


@admin.register(ContactMessage)
class ContactMessageAdmin(ImportExportModelAdmin):
    resource_class = ContactMessageResource
    list_display = ['full_name', 'email', 'phone_number', 'message_preview', 'has_cv', 'created_at']
    list_filter = ['created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'message']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'
    
    def message_preview(self, obj):
        if obj.message:
            return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
        return "No message"
    message_preview.short_description = 'Message'
    
    def has_cv(self, obj):
        return bool(obj.cv_url)
    has_cv.boolean = True
    has_cv.short_description = 'CV Attached'


@admin.register(Approach)
class ApproachAdmin(ImportExportModelAdmin):
    resource_class = ApproachResource
    list_display = ['title', 'description_preview', 'order', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description']
    list_editable = ['order']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order']
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "No description"
    description_preview.short_description = 'Description'


@admin.register(Partner)
class PartnerAdmin(ImportExportModelAdmin):
    resource_class = PartnerResource
    list_display = ['title', 'button_text', 'logo_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'button_text']
    inlines = [PartnerLogoInline]
    readonly_fields = ['created_at', 'updated_at']
    
    def logo_count(self, obj):
        return obj.logos.count()
    logo_count.short_description = 'Logos'


@admin.register(PartnerLogo)
class PartnerLogoAdmin(admin.ModelAdmin):
    list_display = ['id', 'partner', 'image_preview', 'order', 'created_at']
    list_filter = ['partner', 'created_at']
    list_editable = ['order']
    ordering = ['partner', 'order']
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Image Preview'


@admin.register(WorkProcess)
class WorkProcessAdmin(ImportExportModelAdmin):
    resource_class = WorkProcessResource
    list_display = ['title', 'description_preview', 'order', 'image_preview', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description']
    list_editable = ['order']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order']
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "No description"
    description_preview.short_description = 'Description'
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Image Preview'
