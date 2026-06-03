from django.db import models
from django.contrib.auth.models import AbstractUser
import os

class Entrenador(AbstractUser):
    """Modelo de Entrenador - Superusuario del sistema"""
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    foto = models.ImageField(upload_to='entrenadores/', null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    is_trainer = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Entrenador'
        verbose_name_plural = 'Entrenadores'
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.especialidad}"
    
    def delete(self, *args, **kwargs):
        # Eliminar foto al borrar el entrenador
        if self.foto and os.path.isfile(self.foto.path):
            os.remove(self.foto.path)
        super().delete(*args, **kwargs)


class Rutina(models.Model):
    """Modelo de Rutina - Relacionado con Entrenador"""
    NIVEL_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]
    
    nombre = models.CharField(max_length=100)
    duracion = models.IntegerField(help_text="Duración en minutos")
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='rutinas/')
    entrenador = models.ForeignKey(
        Entrenador, 
        on_delete=models.CASCADE, 
        related_name='rutinas',
        null=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Rutina'
        verbose_name_plural = 'Rutinas'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} - {self.nivel}"
    
    def delete(self, *args, **kwargs):
        # Eliminar imagen al borrar la rutina
        if self.imagen and os.path.isfile(self.imagen.path):
            os.remove(self.imagen.path)
        super().delete(*args, **kwargs)