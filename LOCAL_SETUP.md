# 🔧 Local Development Setup

## First Time Setup

After cloning the repository or pulling new changes that update `requirements.txt`, you need to install the dependencies.

### Option 1: Automated Setup (Recommended)

Run the setup script:
```powershell
.\setup.ps1
```

This will:
- ✅ Activate virtual environment (or create if missing)
- ✅ Install all requirements
- ✅ Run database migrations
- ✅ Collect static files

### Option 2: Manual Setup

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input
```

## Common Issues

### ❌ ModuleNotFoundError: No module named 'dj_database_url'

**Solution:**
```powershell
pip install -r requirements.txt
```

Or install specific packages:
```powershell
pip install dj-database-url psycopg2-binary
```

### ❌ No such table: cse_app_chairman

**Solution:**
```powershell
python manage.py migrate
```

### ❌ Static files not loading (locally)

**Solution:**
```powershell
python manage.py collectstatic --no-input
```

## Running the Development Server

```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Run server
python manage.py runserver

# Open browser
# http://127.0.0.1:8000
```

## Creating Superuser (Admin Access)

```powershell
python manage.py createsuperuser
```

Then access admin at: http://127.0.0.1:8000/aDmin_neU_cse/

## Requirements File

The project uses these main packages:
- **Django 5.2.6** - Web framework
- **django-ckeditor** - Rich text editor
- **Pillow** - Image processing
- **whitenoise** - Static file serving
- **gunicorn** - WSGI server (production)
- **dj-database-url** - Database URL parsing (production)
- **psycopg2-binary** - PostgreSQL adapter (production)

## Environment Variables

For local development, you can use default settings (SQLite database, DEBUG=True).

For production, set these environment variables:
- `DATABASE_URL` - PostgreSQL connection URL
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to `False`
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

See `.env.example` for reference.

## Project Structure

```
neu_cse/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── setup.ps1             # Setup script (Windows)
├── build.sh              # Build script (Render)
├── db.sqlite3            # Local database (not in git)
├── neu_cse/              # Project settings
│   ├── settings.py       # Main settings
│   ├── urls.py          # URL configuration
│   └── wsgi.py          # WSGI config
├── cse_app/              # Main application
│   ├── models.py        # Database models
│   ├── views.py         # Views
│   ├── urls.py          # App URLs
│   └── admin.py         # Admin config
├── templates/            # HTML templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User uploaded files
└── staticfiles/         # Collected static files (generated)
```

## Next Steps

1. ✅ Install dependencies (`.\setup.ps1`)
2. ✅ Run migrations (`python manage.py migrate`)
3. ✅ Create superuser (`python manage.py createsuperuser`)
4. ✅ Run server (`python manage.py runserver`)
5. 🚀 Start developing!

For deployment to Render, see `RENDER_DEPLOYMENT.md`.
