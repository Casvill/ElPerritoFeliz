# ----------------------------------------------
# users/views/token_views.py
# ----------------------------------------------
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import Usuario


# ----------------------------------------------
# Custom serializer que usa "documento" en vez de "username"
# ----------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'documento'  # 👈 nuestro campo personalizado

    def validate(self, attrs):
        documento = attrs.get('documento')
        password = attrs.get('password')

        if not documento or not password:
            raise serializers.ValidationError("Se requieren documento y contraseña.")

        try:
            user = Usuario.objects.get(documento=documento)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Usuario no encontrado.")

        if not user.check_password(password):
            raise serializers.ValidationError("Contraseña incorrecta.")

        # ⚠️ Aquí hacemos que el super() use el "username" interno correcto
        data = super().validate({
            self.username_field: documento,
            "password": password
        })

        # Agregar datos extra del usuario
        data["user"] = {
            "id": user.id_usuario,
            "nombres": user.nombres,
            "apellidos": user.apellidos,
            "tipo_usuario": user.tipo_usuario,
        }

        return data


# ----------------------------------------------
# Custom View para emitir tokens JWT
# ----------------------------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
