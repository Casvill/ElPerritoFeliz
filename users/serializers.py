# ----------------------------------------------
# users/serializers.py
# ----------------------------------------------
from rest_framework import serializers
from .models import Usuario
from django.contrib.auth import authenticate

# ----------------------------------------------
# Serializer para creación y visualización de usuarios
# ----------------------------------------------
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # No se muestra en respuestas

    class Meta:
        model = Usuario
        fields = [
            "id_usuario",
            "tipo_usuario",
            "tipo_documento",
            "documento",
            "nombres",
            "apellidos",
            "fecha_nacimiento",
            "fecha_vinculacion",
            "telefono",
            "email",
            "direccion",
            "foto",
            "activo",
            "password",
        ]

    def create(self, validated_data):
        """
        Crea un usuario y guarda la contraseña de forma segura (encriptada).
        """
        password = validated_data.pop("password", None)
        usuario = Usuario(**validated_data)
        if password:
            usuario.set_password(password)
        usuario.save()
        return usuario


# ----------------------------------------------
# Serializer para login de usuario
# ----------------------------------------------
class LoginSerializer(serializers.Serializer):
    documento = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        documento = data.get("documento")
        password = data.get("password")

        if not documento or not password:
            raise serializers.ValidationError("Debe ingresar documento y contraseña.")

        # 🔹 Verificar si el usuario existe
        try:
            user = Usuario.objects.get(documento=documento)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas.")

        # 🔹 Verificar si el usuario está activo
        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo. Contacte al administrador.")

        # 🔹 Autenticación de contraseña
        user = authenticate(
            request=self.context.get("request"),
            documento=documento,
            password=password,
        )
        if not user:
            raise serializers.ValidationError("Credenciales inválidas.")

        data["user"] = user
        return data
