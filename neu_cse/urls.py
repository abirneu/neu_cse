"""
URL configuration for neu_cse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# Admin site customization
admin.site.site_header = "NeU CSE Admin Panel"
admin.site.site_title = "NeU CSE Portal"
admin.site.index_title = "Welcome to NeU CSE Admin Panel"

urlpatterns = [
    path('adm1n_nEu_cSe/', admin.site.urls),
    path('', include('cse_app.urls')),  # Include URLs from cse_app
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
