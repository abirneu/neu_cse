# Django Deployment Fix - Static & Media Files on Render

## Issues Fixed:
1. ✅ Admin panel CSS not loading
2. ✅ Images not showing
3. ✅ Database tables not created
4. ✅ Production configuration

## Changes Made:

### 1. `settings.py` Updates:
- Added `dj_database_url` import for PostgreSQL support
- Database now uses PostgreSQL in production (when DATABASE_URL is set)
- DEBUG mode controlled by environment variable
- SECRET_KEY from environment variable
- ALLOWED_HOSTS from environment variable

### 2. `urls.py` Updates:
- Media files now served in both development and production

### 3. Created `build.sh`:
- Installs dependencies
- Collects static files (fixes admin CSS)
- Runs database migrations (creates tables)

### 4. Updated `requirements.txt`:
- Added `psycopg2-binary` for PostgreSQL
- Added `dj-database-url` for database URL parsing

## Steps to Deploy on Render:

### Step 1: Create PostgreSQL Database on Render
1. Go to Render Dashboard → New → PostgreSQL
2. Name: `neu-cse-db` (or any name)
3. Plan: Free
4. Create Database
5. Copy the **Internal Database URL** (starts with `postgres://`)

### Step 2: Configure Your Web Service on Render
1. Go to your web service settings
2. Add these **Environment Variables**:

```
DATABASE_URL = <paste your PostgreSQL Internal Database URL>
SECRET_KEY = <generate a random secret key>
DEBUG = False
ALLOWED_HOSTS = neu-cse.onrender.com,cse.neu.ac.bd
PYTHON_VERSION = 3.13.6
```

To generate a SECRET_KEY, run this locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 3: Update Build Command
In your Render web service settings:
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn neu_cse.wsgi:application`

### Step 4: Push to GitHub
```bash
git add .
git commit -m "Fix static files and media files for production deployment"
git push origin main
```

### Step 5: Redeploy on Render
- Render will automatically redeploy when you push to GitHub
- Or click "Manual Deploy" → "Clear build cache & deploy"

## How It Works:

### Static Files (Admin CSS):
- `python manage.py collectstatic` collects all static files to `staticfiles/`
- **WhiteNoise** serves these files in production
- Admin CSS/JS are now properly served

### Media Files (Uploaded Images):
- Media files are served via Django's static file serving
- **Note**: Render's filesystem is ephemeral, so uploaded files may be lost on restart
- **Recommendation**: Use cloud storage (AWS S3, Cloudinary) for production images

### Database:
- PostgreSQL database on Render (persistent)
- Migrations run automatically during build
- Tables are created properly

## Testing After Deployment:

1. **Check Admin Panel**: 
   - Visit: `https://neu-cse.onrender.com/aDmin_neU_cse/`
   - Admin CSS should load properly

2. **Check Images**:
   - Visit your homepage
   - Existing images should display

3. **Check Database**:
   - No "table does not exist" errors

## Important Notes:

⚠️ **Media Files on Render**:
- Render's free tier has ephemeral filesystem
- Uploaded files are deleted when the service restarts
- **Solution**: Use cloud storage (recommended)

### Optional: Add Cloud Storage for Media Files

Install django-storages and boto3:
```bash
pip install django-storages boto3
```

Add to `settings.py`:
```python
# For AWS S3 (or similar for Cloudinary)
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
```

## Troubleshooting:

### If admin CSS still not loading:
1. Check Render logs for errors during `collectstatic`
2. Verify WhiteNoise is in MIDDLEWARE
3. Clear browser cache

### If images not showing:
1. Check if image paths are correct in templates
2. Use `{{ MEDIA_URL }}` in templates
3. Consider using cloud storage for production

### If database errors persist:
1. Verify DATABASE_URL is set correctly
2. Check Render logs during migration
3. Ensure PostgreSQL database is running

## Need Help?
- Check Render deployment logs
- Verify all environment variables are set
- Ensure build.sh has execute permissions
