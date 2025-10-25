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
from ..serializers import LoginSerializer
import requests
import os
from rest_framework.decorators import api_view

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
    def post(self, request):
        print(request.data) 
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            return Response({
                "message": "Inicio de sesión exitoso",
                "usuario": {
                    "id": user.id_usuario,
                    "documento": user.documento,
                    "nombres": user.nombres,
                    "apellidos": user.apellidos,
                    "tipo_usuario": user.tipo_usuario,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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