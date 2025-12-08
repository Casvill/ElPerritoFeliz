# attendance/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Asistencia
from .serializers import AsistenciaSerializer
from datetime import date

class AsistenciasView(APIView):
    def get(self, request):
        solo_presentes = request.query_params.get('solo_presentes') == 'true'
        asistencias = Asistencia.objects.all()
        
        if solo_presentes:
            # Ajusta según tu modelo
            asistencias = asistencias.filter(fecha=date.today())
        
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AsistenciaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)