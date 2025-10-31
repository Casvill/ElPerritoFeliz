# ----------------------------------------------
# users/views.py
# ----------------------------------------------
from rest_framework import viewsets
from ..models import Usuario
from ..serializers import UsuarioSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from users.serializers import LoginSerializer
import requests
import os
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from axes.handlers.proxy import AxesProxyHandler

# ----------------------------------------------
# Usuario ViewSet (CRUD básico)
# ----------------------------------------------
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all users (any type) to be viewed or edited.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

#----------------------------------------------------------
class LoginView(APIView):
    """
    Vista de inicio de sesión segura con protección contra fuerza bruta usando django-axes.
    Utiliza un serializer para validar los datos y bloquea temporalmente tras varios intentos fallidos.
    """

    def post(self, request, *args, **kwargs):
        # 1️⃣ Verificar si el usuario o IP ya está bloqueado
        if AxesProxyHandler.is_locked(request):
            return Response(
                {
                    "error": (
                        "Tu cuenta o dirección IP ha sido bloqueada temporalmente "
                        "por múltiples intentos fallidos. Intenta más tarde o contacta al administrador."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # 2️⃣ Validar datos de entrada con el serializer
        serializer = LoginSerializer(data=request.data, context={"request": request})

        if not serializer.is_valid():
            # Axes registra automáticamente los intentos fallidos
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 3️⃣ Autenticar y crear sesión
        user = serializer.validated_data["user"]
        login(request, user)

        # 4️⃣ Responder con la información del usuario
        return Response(
            {
                "message": "Inicio de sesión exitoso",
                "usuario": {
                    "id": user.id_usuario,
                    "documento": user.documento,
                    "nombres": user.nombres,
                    "apellidos": user.apellidos,
                    "tipo_usuario": user.tipo_usuario,
                },
            },
            status=status.HTTP_200_OK,
        )
    
@api_view(["POST"])
def verify_recaptcha(request):
    token = request.data.get("token") or request.data.get("recaptchaToken")
    secret_key = os.getenv("RECAPTCHA_SECRET_KEY")

    if not token:
        return Response({"success": False, "error": "Token no proporcionado"}, status=400)

    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {"secret": secret_key, "response": token}

    r = requests.post(url, data=data)
    result = r.json()

    if result.get("success"):
        return Response({"success": True}, status=200)
    else:
        return Response({"success": False, "error": "Falló la verificación del reCAPTCHA"}, status=400)