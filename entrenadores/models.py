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


from django.db import models
from django.conf import settings

class Rutina(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    duracion = models.IntegerField(help_text='Duración en minutos')
    nivel = models.CharField(max_length=50, choices=[
        ('Principiante', 'Principiante'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ])
    
    # ✅ Imagen opcional
    imagen = models.ImageField(
        upload_to='rutinas/',
        null=True,
        blank=True,
    )
    
    entrenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rutinas'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre