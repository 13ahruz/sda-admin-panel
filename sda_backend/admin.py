"""
Django Admin configuration for SDA Backend models.
Provides comprehensive admin interface with inline editing, filters, and search.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Project, ProjectPhoto, ProjectService, ProjectSolution, PropertySector, SectorInn, PropertySectorProcess,
    News, NewsSection,
    TeamMember, TeamSection, TeamSectionItem,
    Service, ServiceBenefit, ServiceProcess, ServiceWorkProcess,
    About,
    ContactMessage,
    Partner, PartnerLogo,
    WorkProcess
)
from .forms import (
    ProjectAdminForm, ProjectPhotoAdminForm, NewsAdminForm, NewsSectionAdminForm,
    TeamMemberAdminForm, ServiceAdminForm, PartnerLogoAdminForm,
    WorkProcessAdminForm, ServiceProcessAdminForm
)


# ==================== Inline Admins ====================

class ProjectPhotoInline(admin.TabularInline):
    model = ProjectPhoto
    form = ProjectPhotoAdminForm
    extra = 1
    fields = ('image', 'image_url', 'order', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 200px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Preview'


class ProjectServiceInline(admin.TabularInline):
    model = ProjectService
    extra = 1
    fields = ('service', 'order')
    autocomplete_fields = ['service']
    ordering = ['order']


class ProjectSolutionInline(admin.TabularInline):
    model = ProjectSolution
    extra = 1
    fields = ('order', 'title_en', 'title_az', 'title_ru', 'description_en', 'description_az', 'description_ru')
    classes = ('collapse',)
    verbose_name = 'Delivered Solution'
    verbose_name_plural = 'Delivered Solutions'


class SectorInnInline(admin.TabularInline):
    model = SectorInn
    extra = 1
    fields = ('title', 'description', 'order')


class PropertySectorProcessInline(admin.TabularInline):
    model = PropertySectorProcess
    extra = 1
    fields = ('order', 'title_en', 'title_az', 'title_ru', 'description_en', 'description_az', 'description_ru')
    classes = ('collapse',)
    verbose_name = 'Process Step'
    verbose_name_plural = 'Process Steps'


class NewsSectionInline(admin.StackedInline):
    model = NewsSection
    form = NewsSectionAdminForm
    extra = 1
    fields = (
        'order',
        ('heading', 'heading_en', 'heading_az', 'heading_ru'),
        ('content', 'content_en', 'content_az', 'content_ru'),
        'image',
        'image_url'
    )


class TeamSectionItemInline(admin.TabularInline):
    model = TeamSectionItem
    extra = 1
    fields = ('name', 'description', 'photo_url', 'button_text', 'order')


class PartnerLogoInline(admin.TabularInline):
    model = PartnerLogo
    form = PartnerLogoAdminForm
    extra = 1
    fields = ('image', 'image_url', 'order', 'logo_preview')
    readonly_fields = ('logo_preview',)
    
    def logo_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image_url)
        return "No logo"
    logo_preview.short_description = 'Preview'


class ServiceBenefitInline(admin.TabularInline):
    model = ServiceBenefit
    extra = 1
    fields = ('order', 'title_en', 'title_az', 'title_ru', 'description_en', 'description_az', 'description_ru')
    classes = ('collapse',)
    verbose_name = 'Benefit'
    verbose_name_plural = 'Benefits'


class ServiceProcessInline(admin.TabularInline):
    model = ServiceProcess
    form = ServiceProcessAdminForm
    extra = 1
    fields = ('order', 'icon', 'icon_url', 'title_en', 'title_az', 'title_ru', 'description_en', 'description_az', 'description_ru')
    readonly_fields = ('icon_url',)
    classes = ('collapse',)
    verbose_name = 'Service What We Do Item'
    verbose_name_plural = 'Service What We Do Items'


class ServiceWorkProcessInline(admin.TabularInline):
    model = ServiceWorkProcess
    extra = 1
    fields = ('order', 'title_en', 'title_az', 'title_ru', 'description_en', 'description_az', 'description_ru')
    classes = ('collapse',)
    verbose_name = 'Service Process Step'
    verbose_name_plural = 'Service Process Steps'


# ==================== Model Admins ====================

@admin.register(PropertySector)
class PropertySectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_display', 'order', 'featured_projects_display', 'inns_count', 'processes_count', 'projects_count')
    list_editable = ('order',)
    search_fields = ('title_en', 'title_az', 'title_ru', 'title')
    ordering = ('order',)
    inlines = [SectorInnInline, PropertySectorProcessInline]
    
    fieldsets = (
        ('English', {
            'fields': ('title_en', 'description_en')
        }),
        ('Azərbaycan', {
            'fields': ('title_az', 'description_az')
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('Legacy', {
            'fields': ('title', 'description'),
            'classes': ('collapse',)
        }),
        ('Featured Projects', {
            'fields': ('featured_project_1', 'featured_project_2', 'featured_project_3'),
            'description': 'Select up to 3 featured projects for this property sector'
        }),
        ('Settings', {
            'fields': ('order',)
        }),
    )
    
    def title_display(self, obj):
        return obj.title_en or obj.title or f"Sector {obj.id}"
    title_display.short_description = 'Title'
    
    def featured_projects_display(self, obj):
        featured = []
        for project in [obj.featured_project_1, obj.featured_project_2, obj.featured_project_3]:
            if project:
                featured.append(f"{project.slug or project.title_en or f'#{project.id}'}")
        return ", ".join(featured) if featured else "-"
    featured_projects_display.short_description = 'Featured Projects'
    
    def inns_count(self, obj):
        return obj.inns.count()
    inns_count.short_description = 'Inns'
    
    def processes_count(self, obj):
        return obj.process_steps.count() if hasattr(obj, 'process_steps') else 0
    processes_count.short_description = 'Process Steps'
    
    def projects_count(self, obj):
        return obj.projects.count()
    projects_count.short_description = 'Projects'


@admin.register(PropertySectorProcess)
class PropertySectorProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_sector_name', 'title_display', 'order')
    list_filter = ('property_sector__title_en',)
    search_fields = ('title_en', 'title_az', 'title_ru', 'title', 'description_en', 'description_az', 'description_ru')
    list_editable = ('order',)
    ordering = ('property_sector__id', 'order',)
    
    fieldsets = (
        ('Basic', {
            'fields': ('property_sector', 'order')
        }),
        ('English', {
            'fields': ('title_en', 'description_en')
        }),
        ('Azərbaycan', {
            'fields': ('title_az', 'description_az')
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('Legacy', {
            'fields': ('title', 'description'),
            'classes': ('collapse',)
        }),
    )
    
    def title_display(self, obj):
        return obj.title_en or obj.title or f"Process {obj.id}"
    title_display.short_description = 'Title'
    
    def property_sector_name(self, obj):
        return obj.property_sector.title_en or obj.property_sector.title or f"Sector {obj.property_sector.id}"
    property_sector_name.short_description = 'Property Sector'


# SectorInn is managed via PropertySector inline
# @admin.register(SectorInn)
# class SectorInnAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'property_sector', 'order')
#     list_filter = ('property_sector',)
#     search_fields = ('title', 'description')
#     list_editable = ('order',)
#     ordering = ('property_sector', 'order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ('id', 'title_display', 'property_sector', 'client', 'year', 'tag', 'photos_count', 'cover_preview')
    list_filter = ('property_sector', 'year', 'tag')
    search_fields = ('title_en', 'title_az', 'title_ru', 'title', 'client', 'slug')
    list_editable = ('property_sector',)
    ordering = ('-year', '-created_at')
    inlines = [ProjectPhotoInline, ProjectServiceInline, ProjectSolutionInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('slug', 'property_sector', 'client', 'year', 'tag')
        }),
        ('Cover Photo', {
            'fields': ('cover_photo', 'cover_photo_url'),
            'description': 'Upload a new cover photo or enter the URL directly'
        }),
        ('English', {
            'fields': ('title_en', 'description_en', 'about_project_en')
        }),
        ('Azərbaycan', {
            'fields': ('title_az', 'description_az', 'about_project_az')
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru', 'about_project_ru')
        }),
        ('Legacy', {
            'fields': ('title',),
            'classes': ('collapse',)
        }),
    )
    
    def title_display(self, obj):
        return obj.title_en or obj.title or f"Project {obj.id}"
    title_display.short_description = 'Title'
    
    def photos_count(self, obj):
        return obj.photos.count()
    photos_count.short_description = 'Photos'
    
    def cover_preview(self, obj):
        if obj.cover_photo_url:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.cover_photo_url)
        return "No cover"
    cover_preview.short_description = 'Cover'


@admin.register(ProjectSolution)
class ProjectSolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'title_display', 'order')
    list_filter = ('project__title_en',)
    search_fields = ('title_en', 'title_az', 'title_ru', 'description_en', 'description_az', 'description_ru')
    list_editable = ('order',)
    ordering = ('project__id', 'order',)
    
    fieldsets = (
        ('Basic', {
            'fields': ('project', 'order')
        }),
        ('English', {
            'fields': ('title_en', 'description_en')
        }),
        ('Azərbaycan', {
            'fields': ('title_az', 'description_az')
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru')
        }),
    )
    
    def title_display(self, obj):
        return obj.title_en or f"Solution {obj.id}"
    title_display.short_description = 'Title'
    
    def project_name(self, obj):
        return obj.project.title_en or obj.project.title or f"Project {obj.project.id}"
    project_name.short_description = 'Project'


# ProjectPhoto is managed via Project inline
# @admin.register(ProjectPhoto)
# class ProjectPhotoAdmin(admin.ModelAdmin):
#     form = ProjectPhotoAdminForm
#     list_display = ('id', 'project', 'order', 'image_preview')
#     list_filter = ('project',)
#     list_editable = ('order',)
#     ordering = ('project', 'order')
#     fields = ('project', 'image', 'image_url', 'order')
#     
#     def image_preview(self, obj):
#         if obj.image_url:
#             return format_html('<img src="{}" style="max-height: 50px;" />', obj.image_url)
#         return "No image"
#     image_preview.short_description = 'Preview'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title_display', 'tags_display', 'sections_count', 'created_at', 'photo_preview')
    search_fields = ('title', 'title_en', 'title_az', 'title_ru', 'summary')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    inlines = [NewsSectionInline]
    
    fieldsets = (
        ('Photo & Tags', {
            'fields': ('photo', 'photo_url', 'tags'),
            'description': 'Upload a new photo or enter the URL directly. Tags array is legacy.'
        }),
        ('English', {
            'fields': ('title_en', 'summary_en', 'tag_en')
        }),
        ('Azərbaycan', {
            'fields': ('title_az', 'summary_az', 'tag_az')
        }),
        ('Русский', {
            'fields': ('title_ru', 'summary_ru', 'tag_ru')
        }),
        ('Legacy', {
            'fields': ('title', 'summary'),
            'classes': ('collapse',)
        }),
    )
    
    def title_display(self, obj):
        return obj.title_en or obj.title or f"News {obj.id}"
    title_display.short_description = 'Title'
    
    def tags_display(self, obj):
        return ', '.join(obj.tags) if obj.tags else '-'
    tags_display.short_description = 'Tags'
    
    def sections_count(self, obj):
        return obj.sections.count()
    sections_count.short_description = 'Sections'
    
    def photo_preview(self, obj):
        if obj.photo_url:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.photo_url)
        return "No photo"
    photo_preview.short_description = 'Photo'


# NewsSection is managed via News inline
# @admin.register(NewsSection)
# class NewsSectionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'news', 'order', 'heading_display')
#     list_filter = ('news',)
#     list_editable = ('order',)
#     ordering = ('news', 'order')
#     
#     def heading_display(self, obj):
#         return obj.heading_en or obj.heading or f"Section {obj.id}"
#     heading_display.short_description = 'Heading'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    form = TeamMemberAdminForm
    list_display = ('id', 'name_display', 'role_display', 'linkedin_url', 'photo_preview')
    search_fields = ('full_name_en', 'full_name_az', 'full_name_ru', 'full_name', 'role_en', 'role_az', 'role_ru')
    ordering = ('id',)
    
    fieldsets = (
        ('Photo', {
            'fields': ('photo', 'photo_url'),
            'description': 'Upload a new photo or enter the URL directly'
        }),
        ('English', {
            'fields': ('full_name_en', 'role_en', 'bio_en')
        }),
        ('Azərbaycan', {
            'fields': ('full_name_az', 'role_az', 'bio_az')
        }),
        ('Русский', {
            'fields': ('full_name_ru', 'role_ru', 'bio_ru')
        }),
        ('Legacy', {
            'fields': ('full_name', 'role', 'bio'),
            'classes': ('collapse',)
        }),
        ('Additional', {
            'fields': ('linkedin_url',)
        }),
    )
    
    def name_display(self, obj):
        return obj.full_name_en or obj.full_name or f"Member {obj.id}"
    name_display.short_description = 'Name'
    
    def role_display(self, obj):
        return obj.role_en or obj.role or '-'
    role_display.short_description = 'Role'
    
    def photo_preview(self, obj):
        if obj.photo_url:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.photo_url)
        return "No photo"
    photo_preview.short_description = 'Photo'


@admin.register(TeamSection)
class TeamSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'button_text', 'items_count')
    search_fields = ('title',)
    inlines = [TeamSectionItemInline]
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items'


# TeamSectionItem is managed via TeamSection inline
# @admin.register(TeamSectionItem)
# class TeamSectionItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'team_section', 'name', 'order')
#     list_filter = ('team_section',)
#     list_editable = ('order',)
#     ordering = ('team_section', 'order')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm
    list_display = ('id', 'name_display', 'slug', 'order', 'benefits_count', 'processes_count', 'icon_preview')
    search_fields = ('name_en', 'name_az', 'name_ru', 'name', 'slug')
    list_editable = ('order',)
    ordering = ('order',)
    inlines = [ServiceBenefitInline, ServiceProcessInline, ServiceWorkProcessInline]
    
    fieldsets = (
        ('Basic', {
            'fields': ('slug', 'order')
        }),
        ('Images', {
            'fields': (('image', 'image_url'), ('icon', 'icon_url')),
            'description': 'Upload new images or enter URLs directly'
        }),
        ('Featured Projects', {
            'fields': ('featured_project_1', 'featured_project_2'),
            'description': 'Select two projects to feature on this service page'
        }),
        ('English', {
            'fields': ('name_en', 'description_en', 'hero_text_en', 'meta_title_en', 'meta_description_en')
        }),
        ('Azərbaycan', {
            'fields': ('name_az', 'description_az', 'hero_text_az', 'meta_title_az', 'meta_description_az')
        }),
        ('Русский', {
            'fields': ('name_ru', 'description_ru', 'hero_text_ru', 'meta_title_ru', 'meta_description_ru')
        }),
        ('Legacy', {
            'fields': ('name', 'description', 'hero_text', 'meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    def name_display(self, obj):
        return obj.name_en or obj.name or f"Service {obj.id}"
    name_display.short_description = 'Name'
    
    def benefits_count(self, obj):
        return obj.benefits.count() if hasattr(obj, 'benefits') else 0
    benefits_count.short_description = 'Benefits'
    
    def processes_count(self, obj):
        return obj.process_steps.count() if hasattr(obj, 'process_steps') else 0
    processes_count.short_description = 'Process Steps'
    
    def icon_preview(self, obj):
        if obj.icon_url:
            return format_html('<img src="{}" style="max-height: 30px;" />', obj.icon_url)
        return "No icon"
    icon_preview.short_description = 'Icon'


@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_name', 'title_display', 'order')
    list_filter = ('service__name_en',)
    search_fields = ('title_en', 'title_az', 'title_ru', 'title', 'description_en', 'description_az', 'description_ru')
    list_editable = ('order',)
    ordering = ('service__id', 'order',)
    
    fieldsets = (
        ('Basic', {
            'fields': ('service', 'order')
        }),
        ('English', {
            'fields': ('title_en', 'description_en')
        }),
        ('Azərbaycan', {
            'fields': ('title_az', 'description_az')
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('Legacy', {
            'fields': ('title', 'description'),
            'classes': ('collapse',)
        }),
    )
    
    def title_display(self, obj):
        return obj.title_en or obj.title or f"Benefit {obj.id}"
    title_display.short_description = 'Title'
    
    def service_name(self, obj):
        return obj.service.name_en or obj.service.name or f"Service {obj.service.id}"
    service_name.short_description = 'Service'


@admin.register(ServiceProcess)
class ServiceProcessAdmin(admin.ModelAdmin):
    form = ServiceProcessAdminForm
    list_display = ('id', 'service_name', 'title_display', 'order', 'icon_preview')
    list_filter = ('service__name_en',)
    search_fields = ('title_en', 'title_az', 'title_ru', 'title', 'description_en', 'description_az', 'description_ru')
    list_editable = ('order',)
    ordering = ('service__id', 'order',)
    
    fieldsets = (
        ('Basic', {
            'fields': ('service', 'order')
        }),
        ('Icon', {
            'fields': (('icon', 'icon_url'),),
            'description': 'Upload icon or enter URL directly'
        }),
        ('English', {
            'fields': ('title_en', 'description_en')
        }),
        ('Azərbaycan', {
            'fields': ('title_az', 'description_az')
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('Legacy', {
            'fields': ('title', 'description'),
            'classes': ('collapse',)
        }),
    )
    
    def title_display(self, obj):
        return obj.title_en or obj.title or f"Process {obj.id}"
    title_display.short_description = 'Title'
    
    def service_name(self, obj):
        return obj.service.name_en or obj.service.name or f"Service {obj.service.id}"
    service_name.short_description = 'Service'
    
    def icon_preview(self, obj):
        if obj.icon_url:
            return format_html('<img src="{}" style="max-height: 30px;" />', obj.icon_url)
        return "No icon"
    icon_preview.short_description = 'Icon'


@admin.register(ServiceWorkProcess)
class ServiceWorkProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_name', 'title_display', 'order')
    list_filter = ('service__name_en',)
    search_fields = ('title_en', 'title_az', 'title_ru', 'title', 'description_en', 'description_az', 'description_ru')
    list_editable = ('order',)
    ordering = ('service__id', 'order',)
    
    fieldsets = (
        ('Basic', {
            'fields': ('service', 'order')
        }),
        ('English', {
            'fields': ('title_en', 'description_en')
        }),
        ('Azərbaycan', {
            'fields': ('title_az', 'description_az')
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('Legacy', {
            'fields': ('title', 'description'),
            'classes': ('collapse',)
        }),
    )
    
    def title_display(self, obj):
        return obj.title_en or obj.title or f"Process {obj.id}"
    title_display.short_description = 'Title'
    
    def service_name(self, obj):
        return obj.service.name_en or obj.service.name or f"Service {obj.service.id}"
    service_name.short_description = 'Service'


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'years_experience', 'ongoing_projects', 'team_members')
    list_editable = ('years_experience', 'ongoing_projects', 'team_members')
    
    fieldsets = (
        ('Statistics', {
            'fields': ('years_experience', 'ongoing_projects', 'team_members'),
            'description': 'Enter numeric values only (e.g., 10 for "10+ years")'
        }),
    )


# AboutLogo is managed via About inline
# @admin.register(AboutLogo)
# class AboutLogoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'about', 'order', 'logo_preview')
#     list_filter = ('about',)
#     list_editable = ('order',)
#     ordering = ('about', 'order')
#     
#     def logo_preview(self, obj):
#         if obj.image_url:
#             return format_html('<img src="{}" style="max-height: 50px;" />', obj.image_url)
#         return "No logo"
#     logo_preview.short_description = 'Preview'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_display', 'email', 'phone_number', 'status', 'is_read', 'created_at', 'message_type')
    list_filter = ('status', 'is_read', 'created_at', 'property_type')
    search_fields = ('name', 'first_name', 'last_name', 'email', 'phone_number', 'company', 'message')
    list_editable = ('status', 'is_read')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Contact Info', {
            'fields': ('name', 'first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Additional Info', {
            'fields': ('company', 'country', 'property_type')
        }),
        ('Message', {
            'fields': ('message', 'cv_url')
        }),
        ('Status', {
            'fields': ('status', 'is_read', 'created_at', 'updated_at')
        }),
    )
    
    def name_display(self, obj):
        if obj.name:
            return obj.name
        elif obj.first_name or obj.last_name:
            return f"{obj.first_name or ''} {obj.last_name or ''}".strip()
        return '-'
    name_display.short_description = 'Name'
    
    def message_type(self, obj):
        if obj.cv_url:
            return format_html('<span style="color: blue;">Career</span>')
        return format_html('<span style="color: green;">Contact</span>')
    message_type.short_description = 'Type'
    
    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_new', 'mark_as_in_progress', 'mark_as_resolved']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark as unread"
    
    def mark_as_new(self, request, queryset):
        queryset.update(status='new')
    mark_as_new.short_description = "Mark as new"
    
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = "Mark as in progress"
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved')
    mark_as_resolved.short_description = "Mark as resolved"


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_display', 'logos_count')
    search_fields = ('title',)
    inlines = [PartnerLogoInline]
    
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
    )
    
    def title_display(self, obj):
        return obj.title or f"Partner {obj.id}"
    title_display.short_description = 'Title'
    
    def logos_count(self, obj):
        return obj.logos.count()
    logos_count.short_description = 'Logos'


# PartnerLogo is managed via Partner inline
# @admin.register(PartnerLogo)
# class PartnerLogoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'partner', 'order', 'logo_preview')
#     list_filter = ('partner',)
#     list_editable = ('order',)
#     ordering = ('partner', 'order')
#     
#     def logo_preview(self, obj):
#         if obj.image_url:
#             return format_html('<img src="{}" style="max-height: 50px;" />', obj.image_url)
#         return "No logo"
#     logo_preview.short_description = 'Preview'


@admin.register(WorkProcess)
class WorkProcessAdmin(admin.ModelAdmin):
    form = WorkProcessAdminForm
    list_display = ('id', 'title_display', 'order', 'image_preview')
    search_fields = ('title_en', 'title_az', 'title_ru', 'title')
    list_editable = ('order',)
    ordering = ('order',)
    
    fieldsets = (
        ('English', {
            'fields': ('title_en', 'description_en')
        }),
        ('Azərbaycan', {
            'fields': ('title_az', 'description_az')
        }),
        ('Русский', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('Legacy', {
            'fields': ('title', 'description'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('order', 'image', 'image_url'),
            'description': 'Upload a new image or enter the URL directly'
        }),
    )
    
    def title_display(self, obj):
        return obj.title_en or obj.title or f"Process {obj.id}"
    title_display.short_description = 'Title'
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Image'


# Customize admin site
admin.site.site_header = "SDA Consulting Admin Panel"
admin.site.site_title = "SDA Admin"
admin.site.index_title = "Welcome to SDA Consulting Administration"
