# users/views/internaluser_views.py
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from ..models import Usuario
from ..serializers import UsuarioSerializer


class UsuarioInternoViewSet(viewsets.ModelViewSet):
    """
    CRUD y listado filtrable de usuarios internos (ADMIN, DIRECTOR, ENTRENADOR)
    con búsqueda por nombre, apellidos, email o documento.
    """
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombres', 'apellidos', 'email', 'documento']  # 👈 búsqueda por estos campos

    def get_queryset(self):
        # Excluimos clientes
        queryset = Usuario.objects.exclude(tipo_usuario='CLIENTE')

        # Filtros adicionales opcionales
        tipo_usuario = self.request.query_params.get('tipo_usuario')
        fecha_vinculacion_after = self.request.query_params.get('fecha_vinculacion_after')
        fecha_vinculacion_before = self.request.query_params.get('fecha_vinculacion_before')

        if tipo_usuario:
            queryset = queryset.filter(tipo_usuario=tipo_usuario)

        if fecha_vinculacion_after:
            queryset = queryset.filter(fecha_vinculacion__gte=fecha_vinculacion_after)

        if fecha_vinculacion_before:
            queryset = queryset.filter(fecha_vinculacion__lte=fecha_vinculacion_before)

        return queryset

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
