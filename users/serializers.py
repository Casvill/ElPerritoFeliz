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
        extra_kwargs = {
            'password': {'write_only': True},
            'foto': {'required': False, 'allow_null': True, 'allow_blank': True},
        }

    def create(self, validated_data):
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

        try:
            user = Usuario.objects.get(documento=documento)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas.")

        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo. Contacte al administrador.")

        user = authenticate(
            request=self.context.get("request"),
            documento=documento,
            password=password,
        )
        if not user:
            raise serializers.ValidationError("Credenciales inválidas.")

        data["user"] = user
        return data


# ----------------------------------------------
# Serializer para perfil del cliente
# ----------------------------------------------
class UsuarioPerfilSerializer(serializers.ModelSerializer):
    petsCount = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            "id_usuario",
            "tipo_documento",
            "tipo_usuario",
            "documento",
            "nombres",
            "apellidos",
            "fecha_nacimiento",
            "telefono",
            "email",
            "direccion",
            "foto",
            "fecha_registro",
            "petsCount",
        ]
        read_only_fields = ["documento", "tipo_documento"]

        # 🔥🔥🔥 AGREGADO SOLO ESTO para que permita actualizar "foto"
        extra_kwargs = {
            'foto': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
        # 🔥🔥🔥 NADA MÁS, no se tocó nada más.

    def get_petsCount(self, obj):
        return obj.caninos.count()
