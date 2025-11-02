# ----------------------------------------------
# users/internaluser_views.py
# ----------------------------------------------
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Usuario
from ..serializers import UsuarioSerializer

# ----------------------------------------------
# ViewSet para gestionar usuarios internos
# ----------------------------------------------
class UsuarioInternoViewSet(viewsets.ModelViewSet):
    """
    CRUD de usuarios internos (ADMIN, DIRECTOR, ENTRENADOR)
    """
    queryset = Usuario.objects.exclude(tipo_usuario='CLIENTE')
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Crea un usuario interno validando rol y contraseña.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        return Response(
            {"mensaje": "Usuario interno creado exitosamente.", "usuario": UsuarioSerializer(usuario).data},
            status=status.HTTP_201_CREATED
        )