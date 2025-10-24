# ----------------------------------------------
# users/models.py
# ----------------------------------------------
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# ----------------------------------------------
# Custom user manager
# ----------------------------------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, documento, password=None, **extra_fields):
        if not documento:
            raise ValueError('El usuario debe tener un número de documento')
        usuario = self.model(documento=documento, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, documento, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipo_usuario', Usuario.ADMIN)

        return self.create_user(documento, password, **extra_fields)

# ----------------------------------------------
# Custom user model
# ----------------------------------------------
class Usuario(AbstractUser):
    # Roles disponibles
    ADMIN = 'ADMIN'
    DIRECTOR = 'DIRECTOR'
    ENTRENADOR = 'ENTRENADOR'
    CLIENTE = 'CLIENTE'

    TIPO_CHOICES = [
        (ADMIN, 'Administrador'),
        (DIRECTOR, 'Director'),
        (ENTRENADOR, 'Entrenador'),
        (CLIENTE, 'Cliente'),
    ]

    # Quitamos los campos heredados que no usaremos
    username = None
    first_name = None
    last_name = None
    

    # Campos personalizados
    id_usuario = models.BigAutoField(primary_key=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_CHOICES)
    documento = models.CharField(max_length=50, unique=True)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    direccion = models.CharField(max_length=300, blank=True)
    fecha_vinculacion = models.DateField(null=True, blank=True)
    foto = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    # Campos de permisos
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # --- Login con documento ---
    USERNAME_FIELD = 'documento'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'tipo_usuario']

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.tipo_usuario})"
