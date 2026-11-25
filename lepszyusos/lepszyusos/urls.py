"""Główny routing projektu lepszyusos."""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('konto/', include('accounts.urls')),
    path('kursy/', include('kursy.urls')),
    path('admin/', admin.site.urls),
]