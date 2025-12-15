"""
URL configuration for studentrecords project.

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
from django.urls import path, include
from records import views as records_views
from django.contrib.auth import views as auth_views

from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('records/', include('records.urls')),
    path('register/', records_views.register, name='register'),
    path('lecturer-login/', auth_views.LoginView.as_view(template_name='lecturer/login.html'), name='lecturer_login'),
]
