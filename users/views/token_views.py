# ----------------------------------------------
# users/views/token_views.py
# ----------------------------------------------
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, status
from rest_framework.response import Response
from users.models import Usuario
from axes.handlers.proxy import AxesProxyHandler


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'documento'

    def validate(self, attrs):
        request = self.context.get("request")
        documento = attrs.get("documento")
        password = attrs.get("password")

        if not documento or not password:
            raise serializers.ValidationError({"detail": "Se requieren documento y contraseña."})

        handler = AxesProxyHandler()

        # 1️⃣ Verificar bloqueo
        if request and handler.is_locked(request):
            raise serializers.ValidationError({
                "detail": "Tu cuenta o dirección IP ha sido bloqueada temporalmente por múltiples intentos fallidos. Intenta más tarde o contacta al administrador."
            })

        # 2️⃣ Obtener usuario
        try:
            user = Usuario.objects.get(documento=documento)
        except Usuario.DoesNotExist:
            if request:
                handler.user_login_failed(
                    sender=None,
                    credentials={"documento": documento},
                    request=request
                )
            raise serializers.ValidationError({"detail": "Credenciales inválidas."})

        # 🚨 3️⃣ Verificar si el usuario está activo
        if not user.is_active:
            raise serializers.ValidationError({"detail": "Usuario inactivo. Contacte al administrador."})

        # 4️⃣ Verificar contraseña
        if not user.check_password(password):
            if request:
                handler.user_login_failed(
                    sender=None,
                    credentials={"documento": documento},
                    request=request
                )
            raise serializers.ValidationError({"detail": "Credenciales inválidas."})

        # 5️⃣ Login exitoso ✅
        if request:
            handler.user_logged_in(sender=None, request=request, user=user)

        # 6️⃣ Generar tokens JWT
        data = super().validate({
            self.username_field: documento,
            "password": password
        })

        # 7️⃣ Agregar datos extra del usuario
        data["user"] = {
            "id": user.id_usuario,
            "nombres": user.nombres,
            "apellidos": user.apellidos,
            "tipo_usuario": user.tipo_usuario,
        }

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("⚠️ Error inesperado en CustomTokenObtainPairView:", str(e))
            return Response({"detail": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
