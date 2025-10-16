# Media Files Cloud Storage Setup (Optional but Recommended)

## Why Use Cloud Storage?

Render's free tier has **ephemeral filesystem**, meaning:
- ❌ Uploaded files are deleted when service restarts
- ❌ Files are lost during redeployment
- ❌ Not suitable for production media files

**Solutions:**
- ✅ AWS S3 (Pay as you go)
- ✅ Cloudinary (Free tier: 25GB storage, 25GB bandwidth)
- ✅ Backblaze B2 (10GB free)
- ✅ Google Cloud Storage

## Option 1: Cloudinary (Recommended - Free Tier)

### Step 1: Create Cloudinary Account
1. Go to https://cloudinary.com/
2. Sign up for free account
3. Get your credentials from Dashboard:
   - Cloud name
   - API Key
   - API Secret

### Step 2: Install Dependencies
Add to `requirements.txt`:
```
cloudinary==1.41.0
django-cloudinary-storage==0.3.0
```

### Step 3: Update settings.py
```python
# Add to INSTALLED_APPS (before 'django.contrib.staticfiles')
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',  # Add this
    'django.contrib.staticfiles',
    'cloudinary',  # Add this
    'cse_app',
    'ckeditor',
]

# Add at the end of settings.py
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Use Cloudinary for media files in production
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

### Step 4: Add Environment Variables on Render
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

---

## Option 2: AWS S3

### Step 1: Create S3 Bucket
1. Go to AWS Console → S3
2. Create new bucket
3. Enable public access for media files
4. Create IAM user with S3 permissions
5. Get Access Key ID and Secret Access Key

### Step 2: Install Dependencies
Add to `requirements.txt`:
```
boto3==1.35.80
django-storages==1.14.4
```

### Step 3: Update settings.py
```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps
    'storages',
]

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'

# Use S3 for media files in production
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

### Step 4: Add Environment Variables on Render
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_S3_REGION_NAME=us-east-1
```

---

## Option 3: Backblaze B2

### Step 1: Create B2 Account
1. Go to https://www.backblaze.com/b2/
2. Create account (10GB free)
3. Create bucket
4. Generate application key

### Step 2: Install Dependencies
Add to `requirements.txt`:
```
django-storages==1.14.4
b2sdk==1.24.1
```

### Step 3: Update settings.py
```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps
    'storages',
]

# Backblaze B2 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('B2_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('B2_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('B2_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.environ.get('B2_ENDPOINT_URL')
AWS_S3_REGION_NAME = 'us-west-000'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'

# Use B2 for media files in production
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### Step 4: Add Environment Variables on Render
```
B2_ACCESS_KEY_ID=your_key_id
B2_SECRET_ACCESS_KEY=your_secret_key
B2_BUCKET_NAME=your_bucket_name
B2_ENDPOINT_URL=https://s3.us-west-000.backblazeb2.com
```

---

## Migration Guide: Moving Existing Images to Cloud

### For Cloudinary:
```python
# Script to upload existing media files
import os
import cloudinary
import cloudinary.uploader

# Configure Cloudinary
cloudinary.config(
    cloud_name='your_cloud_name',
    api_key='your_api_key',
    api_secret='your_api_secret'
)

# Upload all files in media directory
for root, dirs, files in os.walk('media'):
    for file in files:
        file_path = os.path.join(root, file)
        cloudinary.uploader.upload(file_path, folder='media')
        print(f"Uploaded: {file_path}")
```

### For AWS S3:
```python
# Script to upload existing media files
import boto3
import os

s3 = boto3.client(
    's3',
    aws_access_key_id='your_key',
    aws_secret_access_key='your_secret'
)

bucket_name = 'your_bucket_name'

for root, dirs, files in os.walk('media'):
    for file in files:
        file_path = os.path.join(root, file)
        s3_path = file_path.replace('\\', '/')
        s3.upload_file(file_path, bucket_name, s3_path)
        print(f"Uploaded: {file_path}")
```

---

## Testing Cloud Storage

### 1. Update requirements and settings
### 2. Set environment variables
### 3. Deploy to Render
### 4. Upload a test image via admin panel
### 5. Verify image URL points to cloud storage
### 6. Check image displays correctly on website

---

## Comparison:

| Service | Free Tier | Pros | Cons |
|---------|-----------|------|------|
| **Cloudinary** | 25GB storage, 25GB/month bandwidth | Easy setup, image optimization, CDN | Limited free tier |
| **AWS S3** | 5GB for 12 months | Reliable, scalable, widely used | Requires credit card, complex pricing |
| **Backblaze B2** | 10GB storage, 1GB/day download | Good free tier, affordable | Less known, fewer integrations |
| **Google Cloud** | 5GB | Good integration with Google services | Requires credit card |

**Recommendation**: Start with **Cloudinary** for simplicity and good free tier.

---

## Need Help?

- Cloudinary Docs: https://cloudinary.com/documentation/django_integration
- Django-Storages Docs: https://django-storages.readthedocs.io/
- AWS S3 Django: https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/
