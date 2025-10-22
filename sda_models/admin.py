from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import *
import requests
import os
from django.conf import settings


# Helper function to upload files to backend API
def upload_file_to_backend(file, file_type="image"):
    """Upload file to FastAPI backend and return the URL"""
    try:
        backend_url = getattr(settings, 'BACKEND_UPLOAD_URL', 'https://sdaconsulting.az/api/v1/upload')
        
        files = {'file': (file.name, file.read(), file.content_type)}
        data = {'file_type': file_type}
        
        response = requests.post(backend_url, files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('url')
        else:
            print(f"Upload failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return None


# Base admin class
class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# Image preview mixin
class ImagePreviewMixin:
    def image_preview(self, obj):
        if hasattr(obj, 'photo_url') and obj.photo_url:
            return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;"/>', obj.photo_url)
        elif hasattr(obj, 'cover_photo_url') and obj.cover_photo_url:
            return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;"/>', obj.cover_photo_url)
        elif hasattr(obj, 'image_url') and obj.image_url:
            return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;"/>', obj.image_url)
        elif hasattr(obj, 'icon_url') and obj.icon_url:
            return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;"/>', obj.icon_url)
        elif hasattr(obj, 'logo_url') and obj.logo_url:
            return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;"/>', obj.logo_url)
        return "No image"
    image_preview.short_description = "Preview"


# Custom forms for file upload functionality
class NewsAdminForm(forms.ModelForm):
    photo_upload = forms.ImageField(required=False, help_text="Upload a photo (optional)")
    
    class Meta:
        model = News
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.photo_url:
            self.fields['photo_upload'].help_text = f"Current: {self.instance.photo_url}"


class TeamMemberAdminForm(forms.ModelForm):
    photo_upload = forms.ImageField(required=False, help_text="Upload a photo (optional)")
    
    class Meta:
        model = TeamMember
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.photo_url:
            self.fields['photo_upload'].help_text = f"Current: {self.instance.photo_url}"


class ProjectAdminForm(forms.ModelForm):
    cover_photo_upload = forms.ImageField(required=False, help_text="Upload cover photo (optional)")
    
    class Meta:
        model = Project
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.cover_photo_url:
            self.fields['cover_photo_upload'].help_text = f"Current: {self.instance.cover_photo_url}"


class ServiceAdminForm(forms.ModelForm):
    icon_upload = forms.ImageField(required=False, help_text="Upload icon (optional)")
    
    class Meta:
        model = Service
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.icon_url:
            self.fields['icon_upload'].help_text = f"Current: {self.instance.icon_url}"


class ContactMessageAdminForm(forms.ModelForm):
    cv_upload = forms.FileField(
        required=False,
        help_text="Upload CV file (PDF, DOC, DOCX)"
    )
    
    class Meta:
        model = ContactMessage
        fields = '__all__'
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.cv_url:
            self.fields['cv_upload'].help_text = f"Current CV: {self.instance.cv_url}"


class TeamSectionItemAdminForm(forms.ModelForm):
    photo_upload = forms.ImageField(
        required=False,
        help_text="Upload photo for team section item"
    )
    
    class Meta:
        model = TeamSectionItem
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.photo_url:
            self.fields['photo_upload'].help_text = f"Current photo: {self.instance.photo_url}"


class ProjectPhotoAdminForm(forms.ModelForm):
    image_upload = forms.ImageField(
        required=False,
        help_text="Upload image for project photo"
    )
    
    class Meta:
        model = ProjectPhoto
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.image_url:
            self.fields['image_upload'].help_text = f"Current image: {self.instance.image_url}"


# Inline admin classes
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
    form = ProjectPhotoAdminForm
    extra = 1
    fields = ('image_upload', 'image_url', 'order')
    
    def save_model(self, request, obj, form, change):
        if 'image_upload' in form.cleaned_data and form.cleaned_data['image_upload']:
            uploaded_file = form.cleaned_data['image_upload']
            file_url = upload_file_to_backend(uploaded_file, 'projects')
            if file_url:
                obj.image_url = file_url


class NewsSectionInline(admin.TabularInline):
    model = NewsSection
    extra = 1
    fields = ('heading', 'content', 'image_url', 'order')


class TeamSectionItemInline(admin.TabularInline):
    model = TeamSectionItem
    extra = 1
    fields = ('name', 'description', 'photo_url', 'button_text', 'order')


class PartnerLogoInline(admin.TabularInline):
    model = PartnerLogo
    extra = 1
    fields = ('image_url', 'order')


# Main admin classes
@admin.register(About)
class AboutAdmin(BaseAdmin):
    list_display = ('get_experience', 'get_project_count', 'get_members', 'created_at')
    search_fields = ('experience_en', 'experience_az', 'experience_ru', 'experience')
    list_filter = ('created_at',)
    fieldsets = (
        ('English Fields', {
            'fields': ('experience_en', 'project_count_en', 'members_en')
        }),
        ('Azerbaijani Fields', {
            'fields': ('experience_az', 'project_count_az', 'members_az'),
            'classes': ('collapse',)
        }),
        ('Russian Fields', {
            'fields': ('experience_ru', 'project_count_ru', 'members_ru'),
            'classes': ('collapse',)
        }),
        ('Legacy Fields', {
            'fields': ('experience', 'project_count', 'members'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [AboutLogoInline]
    
    def get_experience(self, obj):
        return obj.experience_en or obj.experience or 'N/A'
    get_experience.short_description = 'Experience'
    
    def get_project_count(self, obj):
        return obj.project_count_en or obj.project_count or 'N/A'
    get_project_count.short_description = 'Projects'
    
    def get_members(self, obj):
        return obj.members_en or obj.members or 'N/A'
    get_members.short_description = 'Members'


@admin.register(AboutLogo)
class AboutLogoAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('about', 'image_preview', 'order', 'created_at')
    list_filter = ('about', 'created_at')
    search_fields = ('about__experience',)
    fields = ('about', 'image_url', 'order', 'created_at', 'updated_at')


@admin.register(PropertySector)
class PropertySectorAdmin(BaseAdmin):
    list_display = ('get_title', 'order', 'created_at')
    search_fields = ('title_en', 'title_az', 'title_ru', 'title', 'description_en', 'description_az', 'description_ru')
    list_filter = ('created_at',)
    fieldsets = (
        ('English Fields', {
            'fields': ('title_en', 'description_en')
        }),
        ('Azerbaijani Fields', {
            'fields': ('title_az', 'description_az'),
            'classes': ('collapse',)
        }),
        ('Russian Fields', {
            'fields': ('title_ru', 'description_ru'),
            'classes': ('collapse',)
        }),
        ('Legacy Fields', {
            'fields': ('title', 'description'),
            'classes': ('collapse',)
        }),
        ('Display', {
            'fields': ('order',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['order']
    inlines = [SectorInnInline]
    
    def get_title(self, obj):
        return obj.title_en or obj.title or f"Sector {obj.id}"
    get_title.short_description = 'Title'


@admin.register(SectorInn)
class SectorInnAdmin(BaseAdmin):
    list_display = ('title', 'property_sector', 'description', 'order', 'created_at')
    list_filter = ('property_sector', 'created_at')
    search_fields = ('title', 'description', 'property_sector__title')
    fields = ('property_sector', 'title', 'description', 'order', 'created_at', 'updated_at')


@admin.register(Project)
class ProjectAdmin(BaseAdmin, ImagePreviewMixin):
    form = ProjectAdminForm
    list_display = ('get_title', 'client', 'year', 'property_sector', 'image_preview', 'created_at')
    list_filter = ('year', 'property_sector', 'created_at')
    search_fields = ('title_en', 'title_az', 'title_ru', 'title', 'client', 'tag')
    fieldsets = (
        ('English Fields', {
            'fields': ('title_en', 'description_en')
        }),
        ('Azerbaijani Fields', {
            'fields': ('title_az', 'description_az'),
            'classes': ('collapse',)
        }),
        ('Russian Fields', {
            'fields': ('title_ru', 'description_ru'),
            'classes': ('collapse',)
        }),
        ('Legacy Fields', {
            'fields': ('title',),
            'classes': ('collapse',)
        }),
        ('Basic Info', {
            'fields': ('slug', 'tag', 'client', 'year', 'property_sector')
        }),
        ('Cover Photo', {
            'fields': ('cover_photo_upload', 'cover_photo_url'),
            'description': 'You can either upload a file or enter a URL directly.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [ProjectPhotoInline]
    
    def get_title(self, obj):
        return obj.title_en or obj.title or f"Project {obj.id}"
    get_title.short_description = 'Title'
    
    def save_model(self, request, obj, form, change):
        if 'cover_photo_upload' in form.cleaned_data and form.cleaned_data['cover_photo_upload']:
            uploaded_file = form.cleaned_data['cover_photo_upload']
            file_url = upload_file_to_backend(uploaded_file, 'projects')
            if file_url:
                obj.cover_photo_url = file_url
        super().save_model(request, obj, form, change)


@admin.register(ProjectPhoto)
class ProjectPhotoAdmin(BaseAdmin, ImagePreviewMixin):
    form = ProjectPhotoAdminForm
    list_display = ('project', 'image_preview', 'order', 'created_at')
    list_filter = ('project', 'created_at')
    search_fields = ('project__title',)
    fieldsets = (
        ('Content', {
            'fields': ('project', 'order')
        }),
        ('Image', {
            'fields': ('image_upload', 'image_url'),
            'description': 'You can either upload a file or enter a URL directly.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if 'image_upload' in form.cleaned_data and form.cleaned_data['image_upload']:
            uploaded_file = form.cleaned_data['image_upload']
            file_url = upload_file_to_backend(uploaded_file, 'projects')
            if file_url:
                obj.image_url = file_url
        super().save_model(request, obj, form, change)


@admin.register(News)
class NewsAdmin(BaseAdmin, ImagePreviewMixin):
    form = NewsAdminForm
    list_display = ('get_title', 'image_preview', 'created_at')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'title_en', 'title_az', 'title_ru', 'summary', 'summary_en', 'summary_az', 'summary_ru', 'tags')
    fieldsets = (
        ('English Fields', {
            'fields': ('title_en', 'summary_en')
        }),
        ('Azerbaijani Fields', {
            'fields': ('title_az', 'summary_az'),
            'classes': ('collapse',)
        }),
        ('Russian Fields', {
            'fields': ('title_ru', 'summary_ru'),
            'classes': ('collapse',)
        }),
        ('Default Fields', {
            'fields': ('title', 'summary', 'tags')
        }),
        ('Photo', {
            'fields': ('photo_upload', 'photo_url'),
            'description': 'You can either upload a file or enter a URL directly.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [NewsSectionInline]
    
    def get_title(self, obj):
        return obj.title_en or obj.title
    get_title.short_description = 'Title'
    
    def save_model(self, request, obj, form, change):
        if 'photo_upload' in form.cleaned_data and form.cleaned_data['photo_upload']:
            uploaded_file = form.cleaned_data['photo_upload']
            file_url = upload_file_to_backend(uploaded_file, 'image')
            if file_url:
                obj.photo_url = file_url
        super().save_model(request, obj, form, change)


@admin.register(NewsSection)
class NewsSectionAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('news', 'get_heading', 'order', 'image_preview', 'created_at')
    list_filter = ('news', 'created_at')
    search_fields = ('heading', 'heading_en', 'heading_az', 'heading_ru', 'content', 'content_en', 'content_az', 'content_ru', 'news__title')
    fieldsets = (
        ('English Fields', {
            'fields': ('heading_en', 'content_en')
        }),
        ('Azerbaijani Fields', {
            'fields': ('heading_az', 'content_az'),
            'classes': ('collapse',)
        }),
        ('Russian Fields', {
            'fields': ('heading_ru', 'content_ru'),
            'classes': ('collapse',)
        }),
        ('Default Fields', {
            'fields': ('news', 'heading', 'content', 'order')
        }),
        ('Image', {
            'fields': ('image_url',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_heading(self, obj):
        return obj.heading_en or obj.heading or 'No heading'
    get_heading.short_description = 'Heading'


@admin.register(TeamMember)
class TeamMemberAdmin(BaseAdmin, ImagePreviewMixin):
    form = TeamMemberAdminForm
    list_display = ('get_full_name', 'get_role', 'image_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'full_name_en', 'full_name_az', 'full_name_ru', 'role', 'role_en', 'role_az', 'role_ru')
    fieldsets = (
        ('English Fields', {
            'fields': ('full_name_en', 'role_en', 'bio_en')
        }),
        ('Azerbaijani Fields', {
            'fields': ('full_name_az', 'role_az', 'bio_az'),
            'classes': ('collapse',)
        }),
        ('Russian Fields', {
            'fields': ('full_name_ru', 'role_ru', 'bio_ru'),
            'classes': ('collapse',)
        }),
        ('Legacy Fields', {
            'fields': ('full_name', 'role', 'bio'),
            'classes': ('collapse',)
        }),
        ('Social & Photo', {
            'fields': ('linkedin_url',)
        }),
        ('Photo', {
            'fields': ('photo_upload', 'photo_url'),
            'description': 'You can either upload a file or enter a URL directly.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.full_name_en or obj.full_name or f"Team Member {obj.id}"
    get_full_name.short_description = 'Full Name'
    
    def get_role(self, obj):
        return obj.role_en or obj.role or 'N/A'
    get_role.short_description = 'Role'
    
    def save_model(self, request, obj, form, change):
        if 'photo_upload' in form.cleaned_data and form.cleaned_data['photo_upload']:
            uploaded_file = form.cleaned_data['photo_upload']
            file_url = upload_file_to_backend(uploaded_file, 'team')
            if file_url:
                obj.photo_url = file_url
        super().save_model(request, obj, form, change)


@admin.register(TeamSection)
class TeamSectionAdmin(BaseAdmin):
    list_display = ('title', 'button_text', 'created_at')
    search_fields = ('title', 'button_text')
    list_filter = ('created_at',)
    fields = ('title', 'button_text', 'created_at', 'updated_at')
    inlines = [TeamSectionItemInline]


@admin.register(TeamSectionItem)
class TeamSectionItemAdmin(BaseAdmin, ImagePreviewMixin):
    form = TeamSectionItemAdminForm
    list_display = ('name', 'team_section', 'description', 'order', 'image_preview', 'created_at')
    list_filter = ('team_section', 'created_at')
    search_fields = ('name', 'description', 'team_section__title')
    fieldsets = (
        ('Basic Info', {
            'fields': ('team_section', 'name', 'description', 'button_text', 'order')
        }),
        ('Photo', {
            'fields': ('photo_upload', 'photo_url'),
            'description': 'You can either upload a file or enter a URL directly.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if 'photo_upload' in form.cleaned_data and form.cleaned_data['photo_upload']:
            uploaded_file = form.cleaned_data['photo_upload']
            file_url = upload_file_to_backend(uploaded_file, 'team_items')
            if file_url:
                obj.photo_url = file_url
        super().save_model(request, obj, form, change)


@admin.register(Service)
class ServiceAdmin(BaseAdmin, ImagePreviewMixin):
    form = ServiceAdminForm
    list_display = ('get_name', 'order', 'image_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'name_en', 'name_az', 'name_ru', 'description', 'description_en', 'description_az', 'description_ru')
    fieldsets = (
        ('English Fields', {
            'fields': ('name_en', 'description_en', 'hero_text_en', 'meta_title_en', 'meta_description_en')
        }),
        ('Azerbaijani Fields', {
            'fields': ('name_az', 'description_az', 'hero_text_az', 'meta_title_az', 'meta_description_az'),
            'classes': ('collapse',)
        }),
        ('Russian Fields', {
            'fields': ('name_ru', 'description_ru', 'hero_text_ru', 'meta_title_ru', 'meta_description_ru'),
            'classes': ('collapse',)
        }),
        ('Legacy Fields', {
            'fields': ('name', 'description', 'hero_text', 'meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Basic Info', {
            'fields': ('slug', 'order')
        }),
        ('Images', {
            'fields': ('icon_upload', 'icon_url', 'image_url'),
            'description': 'You can either upload a file or enter a URL directly.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['order']
    
    def get_name(self, obj):
        return obj.name_en or obj.name or f"Service {obj.id}"
    get_name.short_description = 'Name'
    
    def save_model(self, request, obj, form, change):
        if 'icon_upload' in form.cleaned_data and form.cleaned_data['icon_upload']:
            uploaded_file = form.cleaned_data['icon_upload']
            file_url = upload_file_to_backend(uploaded_file, 'services')
            if file_url:
                obj.icon_url = file_url
        super().save_model(request, obj, form, change)


@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(BaseAdmin):
    list_display = ('title', 'description', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'order', 'created_at', 'updated_at')


@admin.register(ContactMessage)
class ContactMessageAdmin(BaseAdmin):
    form = ContactMessageAdminForm
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'message')
    list_filter = ('created_at',)
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'phone_number', 'email')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('CV/Resume', {
            'fields': ('cv_upload', 'cv_url'),
            'description': 'You can either upload a file or enter a URL directly.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('cv_upload'):
            uploaded_file = form.cleaned_data['cv_upload']
            file_url = upload_file_to_backend(uploaded_file, 'contact')
            if file_url:
                obj.cv_url = file_url
        super().save_model(request, obj, form, change)


@admin.register(Approach)
class ApproachAdmin(BaseAdmin):
    list_display = ('get_title', 'order', 'created_at')
    search_fields = ('title', 'title_en', 'title_az', 'title_ru', 'description', 'description_en', 'description_az', 'description_ru')
    list_filter = ('created_at',)
    fieldsets = (
        ('English Fields', {
            'fields': ('title_en', 'description_en')
        }),
        ('Azerbaijani Fields', {
            'fields': ('title_az', 'description_az'),
            'classes': ('collapse',)
        }),
        ('Russian Fields', {
            'fields': ('title_ru', 'description_ru'),
            'classes': ('collapse',)
        }),
        ('Legacy Fields', {
            'fields': ('title', 'description'),
            'classes': ('collapse',)
        }),
        ('Display', {
            'fields': ('order',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['order']
    
    def get_title(self, obj):
        return obj.title_en or obj.title or f"Approach {obj.id}"
    get_title.short_description = 'Title'


@admin.register(WorkProcess)
class WorkProcessAdmin(BaseAdmin):
    list_display = ('get_title', 'order', 'created_at')
    search_fields = ('title', 'title_en', 'title_az', 'title_ru', 'description', 'description_en', 'description_az', 'description_ru')
    list_filter = ('created_at',)
    fieldsets = (
        ('English Fields', {
            'fields': ('title_en', 'description_en')
        }),
        ('Azerbaijani Fields', {
            'fields': ('title_az', 'description_az'),
            'classes': ('collapse',)
        }),
        ('Russian Fields', {
            'fields': ('title_ru', 'description_ru'),
            'classes': ('collapse',)
        }),
        ('Legacy Fields', {
            'fields': ('title', 'description'),
            'classes': ('collapse',)
        }),
        ('Display', {
            'fields': ('order', 'image_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['order']
    
    def get_title(self, obj):
        return obj.title_en or obj.title or f"Work Process {obj.id}"
    get_title.short_description = 'Title'


@admin.register(Partner)
class PartnerAdmin(BaseAdmin):
    list_display = ('get_title', 'get_button_text', 'created_at')
    search_fields = ('title', 'title_en', 'title_az', 'title_ru', 'button_text', 'button_text_en', 'button_text_az', 'button_text_ru')
    list_filter = ('created_at',)
    fieldsets = (
        ('English Fields', {
            'fields': ('title_en', 'button_text_en')
        }),
        ('Azerbaijani Fields', {
            'fields': ('title_az', 'button_text_az'),
            'classes': ('collapse',)
        }),
        ('Russian Fields', {
            'fields': ('title_ru', 'button_text_ru'),
            'classes': ('collapse',)
        }),
        ('Legacy Fields', {
            'fields': ('title', 'button_text'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [PartnerLogoInline]
    
    def get_title(self, obj):
        return obj.title_en or obj.title or f"Partner {obj.id}"
    get_title.short_description = 'Title'
    
    def get_button_text(self, obj):
        return obj.button_text_en or obj.button_text or 'N/A'
    get_button_text.short_description = 'Button Text'


@admin.register(PartnerLogo)
class PartnerLogoAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('partner', 'image_preview', 'order', 'created_at')
    list_filter = ('partner', 'created_at')
    search_fields = ('partner__title',)
    fields = ('partner', 'logo_url', 'order', 'created_at', 'updated_at')



