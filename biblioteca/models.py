# biblioteca/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Autor(models.Model):
    nombre = models.CharField(max_length=150)
    biografia = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Autores"

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    # Relación de muchos a muchos: Un libro puede tener varios autores
    autores = models.ManyToManyField(Autor, related_name='libros')
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()
    # Gestión de inventario eficiente
    stock_total = models.PositiveIntegerField(default=1)
    stock_disponible = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.titulo

    # Buena práctica: Validación a nivel de modelo para el stock
    def clean(self):
        if self.stock_disponible > self.stock_total:
            raise ValidationError("El stock disponible no puede ser mayor al stock total.")


class Prestamo(models.Model):
    # Relacionamos con el User nativo de Django
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos')
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name='prestamos')
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateTimeField()
    fecha_devolucion_real = models.DateTimeField(blank=True, null=True)
    
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('DEVUELTO', 'Devuelto'),
        ('VENCIDO', 'Vencido'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')

    def __str__(self):
        return f"{self.usuario.username} - {self.libro.titulo}"

    # Lógica de negocio avanzada encapsulada en el modelo
    def clean(self):
        # 1. Validar que la fecha esperada no sea en el pasado
        if self.fecha_devolucion_esperada and self.fecha_devolucion_esperada < timezone.now():
            raise ValidationError("La fecha de devolución esperada no puede ser menor a la fecha actual.")
        
        # 2. Validar stock al CREAR un préstamo nuevo
        if not self.pk:  # Si es un registro nuevo
            if self.libro.stock_disponible < 1:
                raise ValidationError(f"Lo sentimos, no hay stock disponible para el libro: {self.libro.titulo}")

    def save(self, *args, **kwargs):
        self.full_clean()  # Fuerza a Django a ejecutar el método clean() antes de guardar
        
        # Lógica atómica para descontar stock al crear el préstamo
        if not self.pk:
            self.libro.stock_disponible -= 1
            self.libro.save()
            
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Si el préstamo se elimina y NO había sido devuelto aún,
        # le restablecemos el stock al libro antes de borrar el registro.
        if self.estado != 'DEVUELTO':
            self.libro.stock_disponible += 1
            self.libro.save()
            
        # Llamamos al método delete original de Django para que borre la fila
        super().delete(*args, **kwargs)        