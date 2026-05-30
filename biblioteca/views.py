from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Autor, Libro, Prestamo
from .serializers import AutorSerializer, LibroSerializer, PrestamoSerializer

# Decoradores para documentar con Swagger cada acción del CRUD de Autores
@extend_schema_view(
    list=extend_schema(description="Obtiene la lista de todos los autores registrados."),
    create=extend_schema(description="Registra un nuevo autor en el sistema."),
    retrieve=extend_schema(description="Obtiene los detalles de un autor específico por su ID."),
    update=extend_schema(description="Actualiza completamente los datos de un autor."),
    partial_update=extend_schema(description="Actualiza parcialmente los datos de un autor."),
    destroy=extend_schema(description="Elimina un autor del sistema si no tiene libros asociados.")
)
class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all().order_by('nombre')
    serializer_class = AutorSerializer


@extend_schema_view(
    list=extend_schema(description="Obtiene el catálogo de libros con sus autores anidados."),
    create=extend_schema(description="Agrega un nuevo libro al inventario.")
)
class LibroViewSet(viewsets.ModelViewSet):
    serializer_class = LibroSerializer

    def get_queryset(self):
        # BUENA PRÁCTICA (Senior): Usamos prefetch_related para traer los autores en una sola consulta SQL.
        # Esto soluciona el problema de rendimiento N+1 en la base de datos.
        return Libro.objects.prefetch_related('autores').all().order_by('titulo')


class PrestamoViewSet(viewsets.ModelViewSet):
    serializer_class = PrestamoSerializer

    def get_queryset(self):
        # Optimización del Queryset: select_related para las claves foráneas (FK)
        return Prestamo.objects.select_related('usuario', 'libro').all().order_by('-fecha_prestamo')

    def perform_create(self, serializer):
        # BUENA PRÁCTICA: Asignamos automáticamente el usuario que hace la petición al préstamo,
        # si no se envía uno en el payload JSON.
        if 'usuario' not in serializer.validated_data:
            serializer.save(usuario=self.request.user)
        else:
            serializer.save()

    # ENDPOINT PERSONALIZADO: Ruta para devolver un libro de forma limpia
    # URL: /api/v1/prestamos/{id}/devolver/
    @extend_schema(
        request=None,
        responses={200: PrestamoSerializer},
        description="Endpoint personalizado para registrar la devolución de un libro y reestablecer su stock."
    )
    @action(detail=True, methods=['post'], url_path='devolver')
    def devolver_libro(self, request, pk=None):
        prestamo = self.get_object()
        
        if prestamo.estado == 'DEVUELTO':
            return Response(
                {"error": "Este préstamo ya fue devuelto anteriormente."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Actualizamos la lógica de negocio del préstamo de forma atómica
        prestamo.fecha_devolucion_real = timezone.now()
        prestamo.estado = 'DEVUELTO'
        prestamo.save()
        
        # Reestablecemos el stock disponible del libro devuelto
        libro = prestamo.libro
        libro.stock_disponible += 1
        libro.save()
        
        serializer = self.get_serializer(prestamo)
        return Response(serializer.data, status=status.HTTP_200_OK)