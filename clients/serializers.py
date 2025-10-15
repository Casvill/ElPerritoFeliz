# ----------------------------------------------
# clients/serializers.py
# ----------------------------------------------
from rest_framework import serializers
from users.models import Usuario
from django.contrib.auth.hashers import make_password

# ----------------------------------------------
# Serializer for client registration
# ----------------------------------------------
class ClientRegisterSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'correo', 'telefono', 'direccion', 'contrasena']

    def create(self, validated_data):
        contrasena_plana = validated_data.pop('contrasena')
        usuario = Usuario.objects.create(
            tipo_usuario=Usuario.CLIENTE,
            contrasena_hash=make_password(contrasena_plana),
            **validated_data
        )
        return usuario


# ----------------------------------------------
# Serializer for client profile
# ----------------------------------------------
class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'correo', 'telefono', 'direccion', 'foto']
