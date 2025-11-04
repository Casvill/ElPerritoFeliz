# ----------------------------------------------
# dashboard/views/client_dashboard_views.py
# ----------------------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from canines.models import Canino
from enrollments.models import Matricula  # usa el nombre correcto de tu app

# ----------------------------------------------
# Vista del dashboard del cliente autenticado
# ----------------------------------------------
class ClienteDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        caninos = Canino.objects.filter(id_dueno=user).select_related()

        data = []
        for c in caninos:
            # 🔹 Buscar matrícula más reciente
            matricula = Matricula.objects.filter(id_canino=c).order_by('-fecha_fin').first()

            data.append({
                "id": c.id_canino,
                "name": c.nombre,
                "raza": c.raza,
                "tamano": c.tamano,
                "plan": matricula.plan if matricula else "Sin plan",
                "expiresAt": matricula.fecha_fin if matricula else None,
                "absencesThisMonth": 0,  # (luego lo reemplazamos con asistencias reales)
                "avatar": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
                "learning": {"animo": 80, "obediencia": 75, "sociabilidad": 82, "conciencia": 70, "actividad": 77},
                "health": {"conciencia": 85, "mucosas": 80, "pelajePiel": 84, "peso": 79, "abdomen": 81},
            })

        return Response(data, status=status.HTTP_200_OK)
