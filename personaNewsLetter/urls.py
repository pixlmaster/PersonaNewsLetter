"""
URL configuration for personaNewsLetter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from NewsLetters import views

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",  # Replace with your API title
        default_version='v1',    # Specify your API version
        description="Your API description",  # Describe your API
        terms_of_service="https://www.example.com/policies/terms/",  # Link to terms of service
        contact=openapi.Contact(email="contact@example.com"),  # Contact information
        license=openapi.License(name="BSD License"),  # License information
    ),
    public=True,  # Set to True if you want to expose this API publicly
    permission_classes=[permissions.AllowAny],  # Permissions to access the API schema view
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('add_subscriber/', views.add_subscriber, name='add_subscriber'),
    path('add_content/', views.add_content, name='add_content'),
]