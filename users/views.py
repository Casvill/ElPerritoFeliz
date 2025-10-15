# ----------------------------------------------
# users/views.py
# ----------------------------------------------
from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer

# ----------------------------------------------
# Usuario ViewSet (CRUD básico)
# ----------------------------------------------
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all users (any type) to be viewed or edited.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
