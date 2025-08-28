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
        self.backend_url = backend_url or getattr(settings, 'BACKEND_UPLOAD_URL', 'http://web:8000/api/v1/upload')
        super().__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget with current value and file input"""
        if attrs is None:
            attrs = {}
        
        # Basic file input
        file_input = super().render(name, value, attrs, renderer)
        
        # Add current value display if exists
        if value:
            current_display = f'<p>Current: <a href="{value}" target="_blank">{value}</a></p>'
        else:
            current_display = '<p>No file uploaded</p>'
        
        return format_html(
            '<div class="file-upload-widget">{}{}</div>',
            current_display,
            file_input
        )
    
    def value_from_datadict(self, data, files, name):
        """Handle file upload and return URL"""
        print(f"[DEBUG] value_from_datadict called for field: {name}")
        print(f"[DEBUG] Files received: {list(files.keys())}")
        print(f"[DEBUG] Data received: {list(data.keys())}")
        
        upload = files.get(name)
        if upload and hasattr(upload, 'read') and upload.size > 0:
            # Upload file to backend
            try:
                print(f"[DEBUG] Uploading file '{upload.name}' (size: {upload.size}) to: {self.backend_url}")
                
                # Reset file pointer to beginning
                upload.seek(0)
                file_content = upload.read()
                upload.seek(0)  # Reset again for potential reuse
                
                print(f"[DEBUG] File content length: {len(file_content)}")
                print(f"[DEBUG] Content type: {upload.content_type}")
                
                response = requests.post(
                    self.backend_url,
                    files={'file': (upload.name, file_content, upload.content_type or 'application/octet-stream')},
                    timeout=30
                )
                
                print(f"[DEBUG] Upload response: {response.status_code}")
                print(f"[DEBUG] Response headers: {dict(response.headers)}")
                print(f"[DEBUG] Response text: {response.text}")
                
                if response.status_code == 200:
                    result = response.json()
                    url = result.get('url', '')
                    print(f"[DEBUG] Upload successful, URL: {url}")
                    if url:
                        print(f"[DEBUG] Returning URL: {url}")
                        return url
                    else:
                        print("[ERROR] No URL in response")
                        return ''
                else:
                    print(f"[ERROR] Upload failed: Status {response.status_code}, Response: {response.text}")
                    return ''
                    
            except Exception as e:
                print(f"[ERROR] Upload exception: {str(e)}")
                import traceback
                print(f"[ERROR] Traceback: {traceback.format_exc()}")
                return ''
        else:
            print(f"[DEBUG] No file upload for field {name}")
            if upload:
                print(f"[DEBUG] Upload object exists but size: {getattr(upload, 'size', 'unknown')}")
        
        # Handle clear checkbox
        clear = data.get(f'{name}-clear')
        if clear:
            print(f"[DEBUG] Clear checkbox checked for {name}")
            return ''
        
        # Return existing URL if no new file uploaded
        existing_value = data.get(name, '')
        if existing_value and isinstance(existing_value, str):
            print(f"[DEBUG] Returning existing value: {existing_value}")
            return existing_value.strip()
        
        print(f"[DEBUG] No value to return for {name}")
        return ''


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


class BackendUrlField(forms.CharField):
    """
    Field that handles file uploads through the backend and stores URLs
    """
    widget = FileUploadToBackendWidget
    
    def __init__(self, backend_url=None, *args, **kwargs):
        self.backend_url = backend_url
        kwargs.setdefault('max_length', 500)
        kwargs.setdefault('widget', self.widget(backend_url=backend_url))
        super().__init__(*args, **kwargs)


class BackendImageField(forms.CharField):
    """
    Field specifically for image uploads with preview
    """
    widget = ImagePreviewWidget
    
    def __init__(self, backend_url=None, *args, **kwargs):
        self.backend_url = backend_url
        kwargs.setdefault('max_length', 500)
        kwargs.setdefault('widget', self.widget(backend_url=backend_url))
        super().__init__(*args, **kwargs)


class SimpleUrlField(forms.URLField):
    """
    Simple URL field for manual URL entry (no file upload)
    """
    def __init__(self, **kwargs):
        kwargs.setdefault('max_length', 500)
        kwargs.setdefault('help_text', 'Enter the complete URL (e.g., http://example.com/image.jpg)')
        super().__init__(**kwargs)
