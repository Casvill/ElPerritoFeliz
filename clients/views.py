# ----------------------------------------------
# clients/views.py
# ----------------------------------------------
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from users.models import Usuario
from .serializers import ClientRegisterSerializer, ClientProfileSerializer
from django.shortcuts import get_object_or_404

# ----------------------------------------------
# ClientViewSet handles registration and profile
# ----------------------------------------------
class ClientViewSet(viewsets.ViewSet):

    # POST /api/clients/register/
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Cliente registrado correctamente.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET or PUT /api/clients/profile/<correo>/
    @action(detail=True, methods=['get', 'put'])
    def profile(self, request, pk=None):
        usuario = get_object_or_404(Usuario, correo=pk, tipo_usuario=Usuario.CLIENTE)

        if request.method == 'GET':
            serializer = ClientProfileSerializer(usuario)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = ClientProfileSerializer(usuario, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Perfil actualizado correctamente.'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
