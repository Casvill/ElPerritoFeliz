# users/views/internaluser_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Usuario
from ..serializers import UsuarioSerializer

class UsuarioInternoViewSet(viewsets.ModelViewSet):
    """
    CRUD de usuarios internos (ADMIN, DIRECTOR, ENTRENADOR)
    """
    queryset = Usuario.objects.exclude(tipo_usuario='CLIENTE')
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # ✅ Solo ADMIN o DIRECTOR pueden crear internos
        if request.user.tipo_usuario not in ['ADMIN', 'DIRECTOR']:
            return Response(
                {"error": "No tienes permiso para crear usuarios internos."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()

        return Response(
            {
                "mensaje": "Usuario interno creado exitosamente.",
                "usuario": UsuarioSerializer(usuario).data
            },
            status=status.HTTP_201_CREATED
        )
