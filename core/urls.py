"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Importamos las vistas nativas de Simple JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)   

urlpatterns = [
    # CORREGIDO: Cambiar admin.site.split por admin.site.urls
    path('admin/', admin.site.urls), 
    
    # Endpoints de nuestra App
    path('api/v1/', include('biblioteca.urls')),
    
    
    # Endpoints de Autenticación JWT
    # URL para loguearse (recibe username y password, devuelve access y refresh token)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # URL para refrescar el token de acceso cuando expire
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Patrones de URL para la Documentación (Swagger y Redoc)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]