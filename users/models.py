# ----------------------------------------------
# users/models.py
# ----------------------------------------------
from django.db import models

# ----------------------------------------------
# User model (internal and external users)
# ----------------------------------------------
class Usuario(models.Model):
    # ----------------------------------------------
    # Role choices
    # ----------------------------------------------
    ADMIN = 'ADMIN'
    DIRECTOR = 'DIRECTOR'
    ENTRENADOR = 'ENTRENADOR'
    CLIENTE = 'CLIENTE'
    TIPO_CHOICES = [
        (ADMIN, 'Admin'),
        (DIRECTOR, 'Director'),
        (ENTRENADOR, 'Entrenador'),
        (CLIENTE, 'Cliente'),
    ]

    id_usuario = models.BigAutoField(primary_key=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_CHOICES)
    documento = models.CharField(max_length=50, unique=True)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=50, blank=True)  # Only clients often
    direccion = models.CharField(max_length=300, blank=True) # Only clients often
    fecha_vinculacion = models.DateField(null=True, blank=True)  # for internal users
    foto = models.TextField(blank=True)  # URL to image
    contrasena_hash = models.TextField()  # password hash
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.tipo_usuario})"
