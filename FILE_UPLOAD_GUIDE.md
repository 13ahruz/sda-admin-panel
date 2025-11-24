# File Upload Feature - Admin Panel

## Overview

The admin panel now supports **direct file uploads** for images instead of just entering URLs manually. This makes it much easier to manage images.

## Features Added

### ✅ File Upload Fields

All image fields now have two options:
1. **Upload a new file** - Browse and select an image from your computer
2. **Enter URL** - Manually enter an image URL (for existing images)

### 📁 Supported Models

File uploads are now available for:

- **Projects**
  - Cover photo upload
  - Project photos (inline)

- **News**
  - Main photo upload
  - Section images (inline)

- **Team Members**
  - Member photo upload

- **Services**
  - Service image upload
  - Service icon upload

- **About Section**
  - Logo uploads (inline)

- **Partners**
  - Partner logo uploads (inline)

- **Work Processes**
  - Process image upload

## How to Use

### Uploading a New Image

1. Navigate to the model you want to edit (e.g., Projects)
2. Click "Add" or edit an existing record
3. Look for the image upload field (e.g., "Cover Photo Upload")
4. Click "Choose File" and select your image
5. Fill in other required fields
6. Click "Save"

The uploaded file will be:
- Saved to the appropriate uploads directory
- URL automatically generated and saved to the database
- Immediately available in the frontend

### Using an Existing URL

If you already have an image URL:
1. Leave the upload field empty
2. Enter the URL in the corresponding URL field (e.g., "cover_photo_url")
3. Save

### Example: Adding a Project with Photos

```
1. Go to Projects → Add Project
2. Fill in project details (title, client, year, etc.)
3. Upload cover photo:
   - Click "Choose File" under "Cover Photo Upload"
   - Select image from your computer
4. Add project photos:
   - Scroll to "Project Photos" section
   - Click "Choose File" for each photo
   - Set order numbers
5. Click "Save"
```

## File Storage

### Directory Structure

Uploaded files are saved to organized directories:

```
sda/uploads/
├── projects/
│   ├── covers/          # Project cover photos
│   └── photos/          # Project gallery photos
├── news/
│   ├── [main photos]    # News article photos
│   └── sections/        # News section images
├── team/
│   └── members/         # Team member photos
├── services/
│   ├── [main images]    # Service images
│   └── icons/           # Service icons
├── about/
│   └── logos/           # About section logos
├── partners/
│   └── logos/           # Partner logos
└── work-processes/      # Work process images
```

### Generated URLs

The system automatically generates proper URLs:
- Format: `/uploads/{category}/{filename}`
- Example: `/uploads/projects/covers/project1.jpg`

## Technical Details

### How It Works

1. **Upload**: File is uploaded via Django admin form
2. **Save**: File is saved to `sda/uploads/{category}/`
3. **URL Generation**: Path is stored in `*_url` field in database
4. **Access**: FastAPI serves the file from the uploads directory
5. **Display**: Frontend fetches image via the URL

### Form Fields

Each model admin now uses a custom form with:
- `ImageField` for file uploads
- `CharField` (URL) for manual entry
- Both fields are optional
- Upload takes precedence if both are provided

### File Validation

- **Accepted formats**: JPG, JPEG, PNG, GIF, WebP
- **Handled by**: Django's ImageField validation
- **File size**: Depends on your server configuration

## Benefits

### For Administrators
✅ **Easy**: Just click and upload
✅ **Visual**: See preview of uploaded images
✅ **Organized**: Files saved to proper directories
✅ **Flexible**: Can still use URLs if needed

### For Developers
✅ **Clean**: Proper file organization
✅ **Integrated**: Works with existing FastAPI backend
✅ **Maintainable**: Simple form-based approach
✅ **Extendable**: Easy to add more upload fields

## Tips

### Best Practices

1. **Optimize images before upload**
   - Resize to appropriate dimensions
   - Compress to reduce file size
   - Use appropriate format (JPG for photos, PNG for logos)

2. **Use descriptive filenames**
   - Good: `sda-office-building-2024.jpg`
   - Avoid: `IMG_1234.jpg`

3. **Check preview**
   - After upload, verify image displays correctly
   - Check that URL was generated properly

4. **Organize by category**
   - Files are automatically organized
   - Don't manually move files in uploads directory

## Troubleshooting

### Upload button not appearing?
- Refresh the admin page
- Clear browser cache
- Ensure you're on the correct form

### Image not saving?
- Check file size (might be too large)
- Verify file format is supported
- Check uploads directory permissions

### Preview not showing?
- Verify file was actually uploaded
- Check URL field has correct path
- Ensure Docker volume is mounted correctly

### URL field empty after upload?
- Form might have validation errors
- Check other required fields
- Save might have failed - check logs

## Docker Configuration

The admin panel Docker setup includes:
- Volume mount: `../sda/uploads:/app/uploads`
- This ensures files are shared with backend
- Both admin and FastAPI access same uploads directory

## Permissions

Files are saved with appropriate permissions:
- Read access for web server
- Directory structure created automatically
- No manual permission setup needed

## Future Enhancements

Possible improvements:
- [ ] Direct upload to S3/cloud storage
- [ ] Image cropping/resizing in admin
- [ ] Bulk upload functionality
- [ ] Image library/gallery view
- [ ] File usage tracking
- [ ] Automatic thumbnail generation

## Summary

You can now:
1. ✅ Upload images directly in Django admin
2. ✅ Files are organized automatically
3. ✅ URLs are generated automatically
4. ✅ Images work immediately in frontend
5. ✅ Still can use manual URLs if needed

**The admin panel is now much more user-friendly for managing images!** 🎉
