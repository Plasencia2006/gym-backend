from django.db import models
from django.contrib.auth.models import AbstractUser


class Entrenador(AbstractUser):
    """Modelo de usuario personalizado para entrenadores"""
    email = models.EmailField(unique=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    foto = models.ImageField(upload_to='entrenadores/', blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='entrenador_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='entrenador_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    
    class Meta:
        verbose_name = 'Entrenador'
        verbose_name_plural = 'Entrenadores'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Rutina(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    duracion = models.IntegerField(help_text='Duración en minutos')
    nivel = models.CharField(max_length=50, choices=[
        ('Principiante', 'Principiante'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ])
    
    # ❌ ELIMINADO: campo imagen
    
    entrenador = models.ForeignKey(
        'entrenadores.Entrenador',
        on_delete=models.CASCADE,
        related_name='rutinas'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Rutina'
        verbose_name_plural = 'Rutinas'
    
    def __str__(self):
        return self.nombre