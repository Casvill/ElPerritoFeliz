#----------------------------------------------
# Import necessary modules
#----------------------------------------------
from rest_framework import viewsets
from .models import Canino
from .serializers import CaninoSerializer


#----------------------------------------------
# ViewSet for Canino
#----------------------------------------------
class CaninoViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing dogs (Canino model).
    """
    queryset = Canino.objects.all().order_by('nombre')
    serializer_class = CaninoSerializer
