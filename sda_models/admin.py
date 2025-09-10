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
    fields = ('logo_url', 'order')


# Main admin classes
@admin.register(About)
class AboutAdmin(BaseAdmin):
    list_display = ('experience', 'project_count', 'members', 'created_at')
    search_fields = ('experience', 'project_count', 'members')
    list_filter = ('created_at',)
    fields = ('experience', 'project_count', 'members', 'created_at', 'updated_at')
    inlines = [AboutLogoInline]


@admin.register(AboutLogo)
class AboutLogoAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('about', 'image_preview', 'order', 'created_at')
    list_filter = ('about', 'created_at')
    search_fields = ('about__experience',)
    fields = ('about', 'image_url', 'order', 'created_at', 'updated_at')


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
    form = ProjectAdminForm
    list_display = ('title', 'client', 'year', 'property_sector', 'image_preview', 'created_at')
    list_filter = ('year', 'property_sector', 'created_at')
    search_fields = ('title', 'client', 'tag')
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'tag', 'client', 'year', 'property_sector')
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
    list_display = ('title', 'image_preview', 'created_at')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'summary', 'tags')
    fieldsets = (
        ('Content', {
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
    
    def save_model(self, request, obj, form, change):
        if 'photo_upload' in form.cleaned_data and form.cleaned_data['photo_upload']:
            uploaded_file = form.cleaned_data['photo_upload']
            file_url = upload_file_to_backend(uploaded_file, 'image')
            if file_url:
                obj.photo_url = file_url
        super().save_model(request, obj, form, change)


@admin.register(NewsSection)
class NewsSectionAdmin(BaseAdmin, ImagePreviewMixin):
    list_display = ('news', 'heading', 'order', 'image_preview', 'created_at')
    list_filter = ('news', 'created_at')
    search_fields = ('heading', 'content', 'news__title')
    fields = ('news', 'heading', 'content', 'image_url', 'order', 'created_at', 'updated_at')


@admin.register(TeamMember)
class TeamMemberAdmin(BaseAdmin, ImagePreviewMixin):
    form = TeamMemberAdminForm
    list_display = ('full_name', 'role', 'image_preview', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('full_name', 'role')
    fieldsets = (
        ('Basic Info', {
            'fields': ('full_name', 'role')
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
    list_display = ('name', 'description', 'order', 'image_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'order')
        }),
        ('Icon', {
            'fields': ('icon_upload', 'icon_url'),
            'description': 'You can either upload a file or enter a URL directly.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['order']
    
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
    list_display = ('title', 'description', 'order', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    fields = ('title', 'description', 'order', 'created_at', 'updated_at')
    ordering = ['order']


@admin.register(WorkProcess)
class WorkProcessAdmin(BaseAdmin):
    list_display = ('title', 'description', 'order', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    fields = ('title', 'description', 'order', 'image_url', 'created_at', 'updated_at')
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
    fields = ('partner', 'logo_url', 'order', 'created_at', 'updated_at')



