from django import forms
from .models import *
from .widgets import SimpleUrlField


class ProjectSimpleAdminForm(forms.ModelForm):
    """Simple form with URL-only fields for immediate use"""
    cover_photo_url = SimpleUrlField(
        required=False, 
        label="Cover Photo URL",
        help_text="Enter the complete URL (e.g., http://example.com/image.jpg)"
    )
    
    class Meta:
        model = Project
        fields = '__all__'


class PartnerLogoSimpleAdminForm(forms.ModelForm):
    logo_url = SimpleUrlField(
        required=False, 
        label="Logo URL",
        help_text="Enter the complete URL"
    )
    
    class Meta:
        model = PartnerLogo
        fields = '__all__'


class AboutLogoSimpleAdminForm(forms.ModelForm):
    logo_url = SimpleUrlField(
        required=False, 
        label="Logo URL", 
        help_text="Enter the complete URL"
    )
    
    class Meta:
        model = AboutLogo
        fields = '__all__'


class TeamMemberSimpleAdminForm(forms.ModelForm):
    photo_url = SimpleUrlField(
        required=False, 
        label="Photo URL",
        help_text="Enter the complete URL"
    )
    
    class Meta:
        model = TeamMember
        fields = '__all__'


class ServiceSimpleAdminForm(forms.ModelForm):
    icon_url = SimpleUrlField(
        required=False, 
        label="Icon URL",
        help_text="Enter the complete URL"
    )
    
    class Meta:
        model = Service
        fields = '__all__'


class NewsSimpleAdminForm(forms.ModelForm):
    image_url = SimpleUrlField(
        required=False, 
        label="Image URL",
        help_text="Enter the complete URL"
    )
    
    class Meta:
        model = News
        fields = '__all__'


class ApproachSimpleAdminForm(forms.ModelForm):
    icon_url = SimpleUrlField(
        required=False, 
        label="Icon URL",
        help_text="Enter the complete URL"
    )
    
    class Meta:
        model = Approach
        fields = '__all__'


class WorkProcessSimpleAdminForm(forms.ModelForm):
    icon_url = SimpleUrlField(
        required=False, 
        label="Icon URL",
        help_text="Enter the complete URL"
    )
    
    class Meta:
        model = WorkProcess
        fields = '__all__'
