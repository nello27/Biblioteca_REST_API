# biblioteca/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Autor, Libro, Prestamo

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'


class LibroSerializer(serializers.ModelSerializer):
    # Técnica avanzada para el portafolio:
    # Cuando listemos libros, mostraremos los nombres de los autores, no solo sus IDs numéricos.
    autores_detalles = AutorSerializer(many=True, read_only=True, source='autores')

    class Meta:
        model = Libro
        fields = [
            'id', 'titulo', 'isbn', 'fecha_publicacion', 
            'stock_total', 'stock_disponible', 'autores', 'autores_detalles'
        ]
        extra_kwargs = {
            # 'autores' se usará para RECIBIR los IDs al crear [1, 2], 
            # pero 'autores_detalles' mostrará el objeto completo al responder.
            'autores': {'write_only': True} 
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PrestamoSerializer(serializers.ModelSerializer):
    # Detalles de lectura anidados para entregar un JSON limpio y profesional
    usuario_detalle = UserSerializer(read_only=True, source='usuario')
    libro_detalle = LibroSerializer(read_only=True, source='libro')

    class Meta:
        model = Prestamo
        fields = [
            'id', 'usuario', 'usuario_detalle', 'libro', 'libro_detalle', 
            'fecha_prestamo', 'fecha_devolucion_esperada', 'fecha_devolucion_real', 'estado'
        ]
        extra_kwargs = {
            'usuario': {'required': False},
            # BUENA PRÁCTICA: Nadie puede setear la fecha real ni el estado al CREAR
            'fecha_devolucion_real': {'read_only': True},
            'estado': {'read_only': True}
        }

    # Validación adicional en el Serializador para complementar el modelo
    def validate(self, attrs):
        # Aquí puedes meter validaciones cruzadas si fuera necesario.
        # Como ya blindamos el método clean() en el Modelo, DRF heredará gran parte de esa lógica,
        # pero es una buena práctica saber que aquí puedes interceptar los datos antes de que toquen la BD.
        return attrs