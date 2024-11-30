# gas_utility_service/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('services/', include('services.urls')),  # App URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Default auth views
]
