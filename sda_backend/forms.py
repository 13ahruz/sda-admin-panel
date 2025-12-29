"""
Custom forms for file uploads in Django Admin.
Handles image uploads and saves them via the FastAPI backend.
"""
from django import forms
from django.core.files.storage import default_storage
from django.conf import settings
import os
import requests
from .models import (
    Project, ProjectPhoto, News, NewsSection, TeamMember,
    Service, ServiceProcess, About, Partner, PartnerLogo, WorkProcess, PropertySector
)


class ImageUploadMixin:
    """Mixin to handle image uploads via FastAPI backend"""
    
    def save_uploaded_file(self, uploaded_file, path_prefix=''):
        """
        Save uploaded file via FastAPI backend upload endpoint
        Returns the URL of the uploaded file
        """
        if not uploaded_file:
            return None
        
        # For now, save locally and return the path
        # In production, you'd upload to FastAPI backend
        upload_dir = os.path.join(settings.MEDIA_ROOT, path_prefix)
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, uploaded_file.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Return the URL path
        return f"/uploads/{path_prefix}/{uploaded_file.name}" if path_prefix else f"/uploads/{uploaded_file.name}"


class ProjectAdminForm(forms.ModelForm, ImageUploadMixin):
    cover_photo = forms.ImageField(required=False, label='Cover Photo Upload')
    
    class Meta:
        model = Project
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make URL field optional
        if 'cover_photo_url' in self.fields:
            self.fields['cover_photo_url'].required = False
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle cover photo upload
        if self.cleaned_data.get('cover_photo'):
            instance.cover_photo_url = self.save_uploaded_file(
                self.cleaned_data['cover_photo'],
                'projects/covers'
            )
        
        if commit:
            instance.save()
        return instance


class ProjectPhotoAdminForm(forms.ModelForm, ImageUploadMixin):
    image = forms.ImageField(required=False, label='Photo Upload')
    
    class Meta:
        model = ProjectPhoto
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make URL field optional
        if 'image_url' in self.fields:
            self.fields['image_url'].required = False
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle image upload
        if self.cleaned_data.get('image'):
            instance.image_url = self.save_uploaded_file(
                self.cleaned_data['image'],
                'projects/photos'
            )
        
        if commit:
            instance.save()
        return instance
        
        if commit:
            instance.save()
        return instance


class NewsAdminForm(forms.ModelForm, ImageUploadMixin):
    photo = forms.ImageField(required=False, label='Photo Upload')
    
    class Meta:
        model = News
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make URL field optional
        if 'photo_url' in self.fields:
            self.fields['photo_url'].required = False
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle photo upload
        if self.cleaned_data.get('photo'):
            instance.photo_url = self.save_uploaded_file(
                self.cleaned_data['photo'],
                'news'
            )
        
        if commit:
            instance.save()
        return instance


class NewsSectionAdminForm(forms.ModelForm, ImageUploadMixin):
    image = forms.ImageField(required=False, label='Image Upload')
    
    class Meta:
        model = NewsSection
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make URL field optional
        if 'image_url' in self.fields:
            self.fields['image_url'].required = False
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle image upload
        if self.cleaned_data.get('image'):
            instance.image_url = self.save_uploaded_file(
                self.cleaned_data['image'],
                'news/sections'
            )
        
        if commit:
            instance.save()
        return instance


class TeamMemberAdminForm(forms.ModelForm, ImageUploadMixin):
    photo = forms.ImageField(required=False, label='Photo Upload')
    
    class Meta:
        model = TeamMember
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make URL field optional
        if 'photo_url' in self.fields:
            self.fields['photo_url'].required = False
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle photo upload
        if self.cleaned_data.get('photo'):
            instance.photo_url = self.save_uploaded_file(
                self.cleaned_data['photo'],
                'team/members'
            )
        
        if commit:
            instance.save()
        return instance


class ServiceAdminForm(forms.ModelForm, ImageUploadMixin):
    image = forms.ImageField(required=False, label='Image Upload')
    
    class Meta:
        model = Service
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make URL field optional
        if 'image_url' in self.fields:
            self.fields['image_url'].required = False
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle image upload
        if self.cleaned_data.get('image'):
            instance.image_url = self.save_uploaded_file(
                self.cleaned_data['image'],
                'services'
            )
        
        if commit:
            instance.save()
        return instance


class PartnerLogoAdminForm(forms.ModelForm, ImageUploadMixin):
    image = forms.ImageField(required=False, label='Logo Upload')
    
    class Meta:
        model = PartnerLogo
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make URL field optional
        if 'image_url' in self.fields:
            self.fields['image_url'].required = False
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle logo upload
        if self.cleaned_data.get('image'):
            instance.image_url = self.save_uploaded_file(
                self.cleaned_data['image'],
                'partners/logos'
            )
        
        if commit:
            instance.save()
        return instance


class WorkProcessAdminForm(forms.ModelForm, ImageUploadMixin):
    image = forms.ImageField(required=False, label='Image Upload')
    
    class Meta:
        model = WorkProcess
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make URL field optional
        if 'image_url' in self.fields:
            self.fields['image_url'].required = False
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle image upload
        if self.cleaned_data.get('image'):
            instance.image_url = self.save_uploaded_file(
                self.cleaned_data['image'],
                'work-processes'
            )
        
        if commit:
            instance.save()
        return instance


class ServiceProcessAdminForm(forms.ModelForm, ImageUploadMixin):
    icon = forms.ImageField(required=False, label='Icon Upload')
    
    class Meta:
        model = ServiceProcess
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make URL field optional
        if 'icon_url' in self.fields:
            self.fields['icon_url'].required = False
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle icon upload
        icon_file = self.cleaned_data.get('icon')
        if icon_file:
            icon_url = self.save_uploaded_file(icon_file, 'services/icons')
            if icon_url:
                instance.icon_url = icon_url
        
        if commit:
            instance.save()
        return instance


class PropertySectorAdminForm(forms.ModelForm):
    """Custom form for PropertySector to allow selecting projects by slug"""
    featured_project_1_slug = forms.CharField(
        required=False,
        label='Featured Project 1 (Slug)',
        help_text='Enter project slug (e.g., "project-name"). Leave blank to use ID field instead.',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., project-name'})
    )
    featured_project_2_slug = forms.CharField(
        required=False,
        label='Featured Project 2 (Slug)',
        help_text='Enter project slug. Leave blank to use ID field instead.',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., project-name'})
    )
    featured_project_3_slug = forms.CharField(
        required=False,
        label='Featured Project 3 (Slug)',
        help_text='Enter project slug. Leave blank to use ID field instead.',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., project-name'})
    )
    
    class Meta:
        model = PropertySector
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate slug fields from existing IDs if editing
        if self.instance.pk:
            if self.instance.featured_project_1_id:
                try:
                    project = Project.objects.get(id=self.instance.featured_project_1_id)
                    self.fields['featured_project_1_slug'].initial = project.slug
                except Project.DoesNotExist:
                    pass
            
            if self.instance.featured_project_2_id:
                try:
                    project = Project.objects.get(id=self.instance.featured_project_2_id)
                    self.fields['featured_project_2_slug'].initial = project.slug
                except Project.DoesNotExist:
                    pass
            
            if self.instance.featured_project_3_id:
                try:
                    project = Project.objects.get(id=self.instance.featured_project_3_id)
                    self.fields['featured_project_3_slug'].initial = project.slug
                except Project.DoesNotExist:
                    pass
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Convert slugs to IDs
        for i in range(1, 4):
            slug_field = f'featured_project_{i}_slug'
            id_field = f'featured_project_{i}_id'
            
            slug = cleaned_data.get(slug_field)
            project_id = cleaned_data.get(id_field)
            
            # If slug is provided, use it to find the project ID
            if slug:
                try:
                    project = Project.objects.get(slug=slug)
                    cleaned_data[id_field] = project.id
                except Project.DoesNotExist:
                    self.add_error(slug_field, f'Project with slug "{slug}" not found.')
            # If no slug but ID is provided, keep the ID
            elif project_id:
                cleaned_data[id_field] = project_id
            else:
                cleaned_data[id_field] = None
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # The IDs are already set in clean()
        if commit:
            instance.save()
        return instance
