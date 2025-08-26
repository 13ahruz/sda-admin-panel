# 📁 File Upload System for Django Admin Panel

Your Django admin panel now supports both file uploads and URL management, just like your FastAPI backend!

## 🔄 How it Works

### Dual Field System:
Each model now has **two fields** for images:
- **`image_file`** - For uploading files directly in Django admin
- **`image_url`** - Stores the URL (auto-filled when file is uploaded, or can be set manually)

### Examples:
- `AboutLogo`: `image_file` + `image_url`
- `Project`: `cover_photo_file` + `cover_photo_url`
- `ProjectPhoto`: `image_file` + `image_url`
- `News`: `photo_file` + `photo_url`
- `TeamMember`: `photo_file` + `photo_url`
- `Service`: `icon_file` + `icon_url`
- `PartnerLogo`: `image_file` + `image_url`
- `WorkProcess`: `image_file` + `image_url`

## 🎯 Usage Options

### Option 1: Upload File (Recommended)
1. In Django admin, use the **file upload field** (e.g., `image_file`)
2. Select and upload your image
3. The URL field will be **automatically filled** with the file path
4. Your FastAPI backend will see the URL in the database

### Option 2: Manual URL Entry
1. Enter the image URL directly in the **URL field** (e.g., `image_url`)
2. Leave the file field empty
3. Perfect for external images or existing URLs

### Option 3: Backend Compatibility
- Files uploaded via FastAPI backend will show in the URL field
- Files uploaded via Django admin will be accessible to FastAPI backend
- Both systems use the same database and file structure

## 📂 File Organization

Files are organized by type:
```
media/
├── about/logos/           # About section logos
├── projects/
│   ├── covers/           # Project cover photos
│   └── photos/           # Project gallery photos
├── news/photos/          # News photos and section images
├── team/photos/          # Team member photos
├── services/icons/       # Service icons
├── partners/logos/       # Partner logos
└── work_processes/images/# Work process images
```

## 🔧 Backend Compatibility

### Database Fields:
- **Existing URL fields remain unchanged** - no data loss
- **New file fields added** - optional, for admin uploads
- **Auto-sync**: File uploads automatically update URL fields

### FastAPI Integration:
```python
# Your FastAPI backend will see URLs like:
"image_url": "/media/projects/covers/uuid-filename.jpg"
"cover_photo_url": "/media/projects/covers/uuid-filename.jpg"
```

### File Access:
- Django admin uploads: `http://admin-panel:8001/media/path/to/file.jpg`
- FastAPI backend: Can access same files via shared volume
- URLs work in both systems

## 🚀 Deployment Update

The Docker setup now includes proper media file handling:

```bash
# Stop and restart with file upload support
docker-compose -f docker-compose.simple.yml down
docker-compose -f docker-compose.simple.yml up -d --build
```

## 📝 Admin Interface Changes

### List Views:
- **Image previews** work with both uploaded files and URLs
- **File upload fields** in inline editors
- **Auto-populated URLs** when files are uploaded

### Edit Forms:
- Upload field + readonly URL field
- Upload file OR enter URL manually
- Image preview for both methods

## 🔒 File Security

- Files are uploaded with **UUID filenames** to prevent conflicts
- **File type validation** (images only)
- **Size limits** to prevent abuse
- **Organized directory structure**

## 🎉 Benefits

✅ **Backward Compatible** - All existing URLs still work
✅ **Dual Input** - Upload files OR enter URLs
✅ **Auto URLs** - File uploads create URLs automatically  
✅ **FastAPI Compatible** - Same database structure
✅ **Image Previews** - See images in admin lists
✅ **Organized Storage** - Clean file organization

Your admin panel now handles files exactly like your FastAPI backend! 🎊
