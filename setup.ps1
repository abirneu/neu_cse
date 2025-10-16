# Setup Script for Local Development
# Run this after cloning the repository

Write-Host "🚀 Setting up NeU CSE Django Project..." -ForegroundColor Green

# Activate virtual environment
Write-Host "`n📦 Activating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found. Creating one..." -ForegroundColor Red
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment created and activated" -ForegroundColor Green
}

# Install requirements
Write-Host "`n📥 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run migrations
Write-Host "`n🗄️ Running database migrations..." -ForegroundColor Yellow
python manage.py migrate

# Collect static files
Write-Host "`n📁 Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --no-input

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`n🎯 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Create superuser: python manage.py createsuperuser" -ForegroundColor White
Write-Host "  2. Run server: python manage.py runserver" -ForegroundColor White
Write-Host "  3. Open browser: http://127.0.0.1:8000" -ForegroundColor White
