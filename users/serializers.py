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
#----------------------------------------------
# users/serializers.py
#----------------------------------------------
from rest_framework import serializers
from .models import Usuario
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    documento = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        documento = data.get("documento")
        password = data.get("password")

        if not documento or not password:
            raise serializers.ValidationError("Debe ingresar documento y contraseña")

        # 🔹 Verificar si el usuario existe
        try:
            user = Usuario.objects.get(documento=documento)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas")

        # 🔹 Verificar si está inactivo
        if not user.is_active:
            print("Usuario inactivo")
            raise serializers.ValidationError("Usuario inactivo, contacte al administrador.")

        # 🔹 Autenticar contraseña
        user = authenticate(request=self.context.get('request'), documento=documento, password=password)
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")

        data["user"] = user
        return data
