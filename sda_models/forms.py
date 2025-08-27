from django import forms
from django.conf import settings
from .models import (
    Project, ProjectPhoto, PartnerLogo, AboutLogo, 
    Service, News, TeamMember, TeamSectionItem, WorkProcess
)
from .widgets import BackendImageField


class ProjectAdminForm(forms.ModelForm):
    cover_photo_url = BackendImageField(
        label="Cover Photo",
        help_text="Upload an image file or enter a URL",
        required=False,
        backend_url=getattr(settings, 'BACKEND_UPLOAD_URL', 'http://sda_web_1:8000/upload')
    )
    
    class Meta:
        model = Project
        fields = '__all__'


class ProjectPhotoAdminForm(forms.ModelForm):
    image_url = BackendImageField(
        label="Photo",
        help_text="Upload an image file or enter a URL",
        required=True,
        backend_url=getattr(settings, 'BACKEND_UPLOAD_URL', 'http://sda_web_1:8000/upload')
    )
    
    class Meta:
        model = ProjectPhoto
        fields = '__all__'


class PartnerLogoAdminForm(forms.ModelForm):
    image_url = BackendImageField(
        label="Logo",
        help_text="Upload an image file or enter a URL",
        required=True,
        backend_url=getattr(settings, 'BACKEND_UPLOAD_URL', 'http://sda_web_1:8000/upload')
    )
    
    class Meta:
        model = PartnerLogo
        fields = '__all__'


class AboutLogoAdminForm(forms.ModelForm):
    image_url = BackendImageField(
        label="Logo",
        help_text="Upload an image file or enter a URL",
        required=True,
        backend_url=getattr(settings, 'BACKEND_UPLOAD_URL', 'http://sda_web_1:8000/upload')
    )
    
    class Meta:
        model = AboutLogo
        fields = '__all__'


class ServiceAdminForm(forms.ModelForm):
    icon_url = BackendImageField(
        label="Icon",
        help_text="Upload an image file or enter a URL",
        required=True,
        backend_url=getattr(settings, 'BACKEND_UPLOAD_URL', 'http://sda_web_1:8000/upload')
    )
    
    class Meta:
        model = Service
        fields = '__all__'


class NewsAdminForm(forms.ModelForm):
    image_url = BackendImageField(
        label="Image",
        help_text="Upload an image file or enter a URL",
        required=True,
        backend_url=getattr(settings, 'BACKEND_UPLOAD_URL', 'http://sda_web_1:8000/upload')
    )
    
    class Meta:
        model = News
        fields = '__all__'


class TeamMemberAdminForm(forms.ModelForm):
    photo_url = BackendImageField(
        label="Photo",
        help_text="Upload an image file or enter a URL",
        required=True,
        backend_url=getattr(settings, 'BACKEND_UPLOAD_URL', 'http://sda_web_1:8000/upload')
    )
    
    class Meta:
        model = TeamMember
        fields = '__all__'


class TeamSectionItemAdminForm(forms.ModelForm):
    photo_url = BackendImageField(
        label="Photo",
        help_text="Upload an image file or enter a URL",
        required=True,
        backend_url=getattr(settings, 'BACKEND_UPLOAD_URL', 'http://sda_web_1:8000/upload')
    )
    
    class Meta:
        model = TeamSectionItem
        fields = '__all__'


class WorkProcessAdminForm(forms.ModelForm):
    image_url = BackendImageField(
        label="Image",
        help_text="Upload an image file or enter a URL",
        required=True,
        backend_url=getattr(settings, 'BACKEND_UPLOAD_URL', 'http://sda_web_1:8000/upload')
    )
    
    class Meta:
        model = WorkProcess
        fields = '__all__'
