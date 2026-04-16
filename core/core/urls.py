from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Оцей рядок активує адмінку
    path('', include('labs.urls')),   # Твої лабораторні
]