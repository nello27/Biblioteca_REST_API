from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AutorViewSet, LibroViewSet, PrestamoViewSet

# Creamos el router estándar de DRF
router = DefaultRouter()

# Registramos nuestros ViewSets con sus respectivos prefijos de URL
router.register(r'autores', AutorViewSet, basename='autor')
router.register(r'libros', LibroViewSet, basename='libro')
router.register(r'prestamos', PrestamoViewSet, basename='prestamo')

# Las URLs de la aplicación simplemente heredan las rutas generadas por el router
urlpatterns = [
    path('', include(router.urls)),
]