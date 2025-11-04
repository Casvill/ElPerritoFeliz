# ----------------------------------------------
# users/models.py
# ----------------------------------------------
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# ----------------------------------------------
# Administrador de usuarios personalizado
# ----------------------------------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, documento, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el documento y la contraseña proporcionados.
        """
        if not documento:
            raise ValueError("El usuario debe tener un número de documento")

        usuario = self.model(documento=documento, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, documento, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con todos los permisos.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("tipo_usuario", Usuario.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(documento, password, **extra_fields)


# ----------------------------------------------
# Modelo de usuario personalizado
# ----------------------------------------------
class Usuario(AbstractUser):
    # ----------------------------------------------
    # Roles disponibles
    # ----------------------------------------------
    ADMIN = "ADMIN"
    DIRECTOR = "DIRECTOR"
    ENTRENADOR = "ENTRENADOR"
    CLIENTE = "CLIENTE"

    TIPO_CHOICES = [
        (ADMIN, "Administrador"),
        (DIRECTOR, "Director"),
        (ENTRENADOR, "Entrenador"),
        (CLIENTE, "Cliente"),
    ]

    # ----------------------------------------------
    # Tipos de documento disponibles
    # ----------------------------------------------
    CC = "CC"
    TI = "TI"
    CE = "CE"
    PAS = "PAS"

    TIPO_DOC_CHOICES = [
        (CC, "Cédula de ciudadanía"),
        (TI, "Tarjeta de identidad"),
        (CE, "Cédula de extranjería"),
        (PAS, "Pasaporte"),
    ]

    # ----------------------------------------------
    # Eliminamos los campos que no usaremos del AbstractUser
    # ----------------------------------------------
    username = None
    first_name = None
    last_name = None

    # ----------------------------------------------
    # Campos personalizados
    # ----------------------------------------------
    id_usuario = models.BigAutoField(primary_key=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_CHOICES)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOC_CHOICES)
    documento = models.CharField(max_length=50, unique=True)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_vinculacion = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    direccion = models.CharField(max_length=300, blank=True)
    foto = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    # ----------------------------------------------
    # Campos de permisos
    # ----------------------------------------------
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # ----------------------------------------------
    # Configuración para inicio de sesión
    # ----------------------------------------------
    USERNAME_FIELD = "documento"
    REQUIRED_FIELDS = ["nombres", "apellidos", "tipo_usuario", "email"]

    # ----------------------------------------------
    # Asignar el administrador personalizado
    # ----------------------------------------------
    objects = UsuarioManager()

    # ----------------------------------------------
    # Representación en texto del modelo
    # ----------------------------------------------
    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.tipo_usuario})"