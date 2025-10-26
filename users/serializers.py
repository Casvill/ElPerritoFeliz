# ----------------------------------------------
# users/serializers.py
# ----------------------------------------------
from rest_framework import serializers
from .models import Usuario
from django.contrib.auth import authenticate

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

# ----------------------------------------------
# Login serializer
# ----------------------------------------------
class LoginSerializer(serializers.Serializer):
    documento = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        documento = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        documento = data.get("documento")
        password = data.get("password")

        if documento and password:
            user = authenticate(documento=documento, password=password)
            if not user:
                raise serializers.ValidationError("Credenciales inválidas")
        else:
            raise serializers.ValidationError("Debe ingresar documento y contraseña")

        data["user"] = user
        return data