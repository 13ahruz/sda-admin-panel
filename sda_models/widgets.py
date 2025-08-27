import requests
from django import forms
from django.conf import settings
from django.utils.html import format_html
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.utils.safestring import mark_safe


class FileUploadToBackendWidget(forms.ClearableFileInput):
    """
    Widget that uploads files to the backend API and stores the returned URL
    """
    
    def __init__(self, backend_url=None, *args, **kwargs):
        self.backend_url = backend_url or getattr(settings, 'BACKEND_UPLOAD_URL', 'http://localhost:8000/upload')
        super().__init__(*args, **kwargs)
    
    def format_value(self, value):
        """Display current URL value"""
        if isinstance(value, str) and value:
            return value
        return None
    
    def value_from_datadict(self, data, files, name):
        """Handle file upload and return URL"""
        upload = files.get(name)
        if upload:
            # Upload file to backend
            try:
                response = requests.post(
                    self.backend_url,
                    files={'file': (upload.name, upload.read(), upload.content_type)}
                )
                if response.status_code == 200:
                    result = response.json()
                    return result.get('url', '')
                else:
                    raise forms.ValidationError(f"Upload failed: {response.text}")
            except Exception as e:
                raise forms.ValidationError(f"Upload error: {str(e)}")
        
        # Return existing URL if no new file uploaded
        return data.get(name, '')


class ImagePreviewWidget(FileUploadToBackendWidget):
    """
    Widget that shows image preview for uploaded images
    """
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        
        if value:
            preview_html = format_html(
                '<div style="margin-top: 10px;">'
                '<p><strong>Current image:</strong></p>'
                '<img src="{}" style="max-height: 150px; max-width: 300px; border: 1px solid #ddd; padding: 5px;" />'
                '<p><small>URL: <a href="{}" target="_blank">{}</a></small></p>'
                '</div>',
                value, value, value
            )
            html += preview_html
        
        return mark_safe(html)


class BackendUrlField(forms.URLField):
    """
    Field that handles file uploads through the backend
    """
    widget = FileUploadToBackendWidget
    
    def __init__(self, backend_url=None, *args, **kwargs):
        self.backend_url = backend_url
        kwargs.setdefault('widget', self.widget(backend_url=backend_url))
        super().__init__(*args, **kwargs)


class BackendImageField(BackendUrlField):
    """
    Field specifically for image uploads with preview
    """
    widget = ImagePreviewWidget
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', self.widget(backend_url=kwargs.pop('backend_url', None)))
        super().__init__(*args, **kwargs)
