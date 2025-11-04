# ----------------------------------------------
# users/views/profile_views.py
# ----------------------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import Usuario
from users.serializers import UsuarioPerfilSerializer

# ----------------------------------------------
# Vista del perfil del cliente autenticado
# ----------------------------------------------
class ClientePerfilView(APIView):
    """
    Permite al cliente autenticado ver y actualizar su perfil.
    """
    permission_classes = [IsAuthenticated]

    # ----------------------------------------------
    # Obtener datos del perfil
    # ----------------------------------------------
    def get(self, request):
        user = request.user
        serializer = UsuarioPerfilSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ----------------------------------------------
    # Actualizar datos del perfil
    # ----------------------------------------------
    def put(self, request):
        user = request.user
        serializer = UsuarioPerfilSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Perfil actualizado correctamente.", "usuario": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
