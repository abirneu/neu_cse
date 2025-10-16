# Quick Deployment Checklist

## ✅ Files Created/Updated:
- [x] `build.sh` - Build script for Render
- [x] `settings.py` - Updated for production
- [x] `urls.py` - Media files serving fixed
- [x] `requirements.txt` - Added PostgreSQL support
- [x] `.gitignore` - Database excluded
- [x] `.env.example` - Environment variables template

## 📋 Before Deploying to Render:

### 1. Install dependencies locally (optional, for testing):
```powershell
pip install -r requirements.txt
```

### 2. Test collectstatic locally:
```powershell
python manage.py collectstatic --no-input
```

### 3. Commit and push to GitHub:
```powershell
git add .
git commit -m "Fix static and media files for production deployment"
git push origin main
```

## 🚀 On Render Dashboard:

### A. Create PostgreSQL Database:
1. Click "New +" → "PostgreSQL"
2. Name: `neu-cse-db`
3. Database: `neu_cse`
4. User: (auto-generated)
5. Region: Same as your web service
6. Plan: **Free**
7. Click "Create Database"
8. **Copy the "Internal Database URL"** (you'll need this)

### B. Configure Web Service:

#### Environment Variables:
Add these in Settings → Environment:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `<paste Internal Database URL from PostgreSQL>` |
| `SECRET_KEY` | `<generate using command below>` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `neu-cse.onrender.com,cse.neu.ac.bd` |
| `PYTHON_VERSION` | `3.13.6` |

**Generate SECRET_KEY locally:**
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Build & Start Commands:
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn neu_cse.wsgi:application`

#### Auto-Deploy:
- ✅ Enable "Auto-Deploy" from GitHub

### C. Deploy:
1. Click "Manual Deploy" → "Clear build cache & deploy"
2. Wait for deployment to complete (3-5 minutes)
3. Check logs for any errors

## ✅ Verify Deployment:

### 1. Check Homepage:
```
https://neu-cse.onrender.com/
```

### 2. Check Admin Panel (CSS should load):
```
https://neu-cse.onrender.com/aDmin_neU_cse/
```

### 3. Create Superuser (if needed):
```powershell
# In Render Shell (Settings → Shell)
python manage.py createsuperuser
```

## 🐛 Troubleshooting:

### Admin CSS not loading:
1. Check Render logs: Look for `collectstatic` errors
2. Verify WhiteNoise in MIDDLEWARE
3. Check STATIC_ROOT and STATIC_URL settings
4. Clear browser cache (Ctrl+Shift+R)

### Images not showing:
1. Check MEDIA_URL and MEDIA_ROOT in settings
2. Verify images exist in database
3. Re-upload images in admin
4. **Note**: Consider cloud storage for production

### Database errors:
1. Verify DATABASE_URL in environment variables
2. Check PostgreSQL database is running
3. Look for migration errors in logs
4. Try manual migration in Shell: `python manage.py migrate`

### Build fails:
1. Check `build.sh` has correct permissions
2. Verify all packages in requirements.txt are available
3. Check Python version compatibility

## 📝 Important Notes:

⚠️ **Media Files Warning**:
- Render's free tier uses **ephemeral storage**
- Uploaded images are **deleted on restart/redeploy**
- **Solution**: Use AWS S3, Cloudinary, or similar for production images

⚠️ **Database**:
- PostgreSQL on Render is persistent (data won't be lost)
- Free tier has 90-day limit for inactivity
- Backup important data regularly

⚠️ **Performance**:
- Free tier "spins down" after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- Consider paid tier for production use

## 🎯 Next Steps After Successful Deployment:

1. **Upload content** through admin panel
2. **Configure DNS** to point cse.neu.ac.bd to Render
3. **Set up cloud storage** for media files (recommended)
4. **Enable HTTPS** (automatic on Render)
5. **Monitor logs** for errors
6. **Set up backups** for database

## 🔗 Useful Links:

- Render Dashboard: https://dashboard.render.com
- Render Docs: https://render.com/docs
- Django Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
