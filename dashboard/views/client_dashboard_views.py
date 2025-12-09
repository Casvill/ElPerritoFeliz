# ----------------------------------------------
# dashboard/views/client_dashboard_views.py
# ----------------------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import date
from canines.models import Canino
from enrollments.models import Matricula
from attendance.models import Asistencia, Aprendizaje, CondicionFisica


class ClienteDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def normalizar_porcentaje(self, valor, minimo, maximo):
        """Convierte un valor numérico a escala 0–100."""
        if valor is None:
            return None
        if valor < minimo:
            return 0
        if valor > maximo:
            return 100
        return round(((valor - minimo) / (maximo - minimo)) * 100)

    def interpretar_texto_bueno(self, texto):
        """Devuelve 100 si contiene palabras positivas, 40 si vacío, 10 si es negativo."""
        if not texto:
            return 40
        t = texto.lower()
        positivos = ["normal", "bien", "óptimo", "sano", "brillante"]
        negativos = ["mal", "opaco", "enrojecido", "inflamado", "pálido"]

        if any(p in t for p in positivos):
            return 100
        if any(n in t for n in negativos):
            return 20
        return 60  # neutral

    def get(self, request):
        user = request.user
        hoy = date.today()
        mes_inicio = hoy.replace(day=1)

        caninos = Canino.objects.filter(id_dueno=user)
        data = []

        for c in caninos:

            # MATRÍCULA
            matricula = Matricula.objects.filter(id_canino=c).order_by('-fecha_fin').first()

            # ASISTENCIAS DEL MES
            asistencias_mes = Asistencia.objects.filter(
                id_canino=c,
                fecha__gte=mes_inicio,
                fecha__lte=hoy
            ).count()

            # APRENDIZAJE (último)
            aprendizaje = Aprendizaje.objects.filter(id_canino=c).order_by('-id_aprendizaje').first()
            if aprendizaje:
                learning = {
                    "animo": aprendizaje.estado_animo,
                    "obediencia": aprendizaje.obediencia,
                    "sociabilidad": aprendizaje.sociabilidad,
                    "conciencia": aprendizaje.conciencia,
                    "actividad": aprendizaje.actividad,
                }
            else:
                learning = None

            # SALUD (último registro)
            condicion = CondicionFisica.objects.filter(id_canino=c).order_by('-id_condicion').first()
            if condicion:
                health = {
                    "conciencia": None,  # no existe en el modelo de condición física
                    "mucosas": self.interpretar_texto_bueno(condicion.color_mucosas),
                    "pelajePiel": self.interpretar_texto_bueno(condicion.pelaje_piel),
                    "peso": self.normalizar_porcentaje(condicion.peso, 3, 40),
                    "abdomen": self.interpretar_texto_bueno(condicion.observaciones),
                }
            else:
                health = None

            # RESPUESTA POR CANINO
            data.append({
                "id": c.id_canino,
                "name": c.nombre,
                "raza": c.raza,
                "plan": matricula.plan if matricula else "Sin plan",
                "expiresAt": matricula.fecha_fin if matricula else None,
                "absencesThisMonth": asistencias_mes,
                "avatar": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
                "learning": learning,
                "health": health,
            })

        return Response(data, status=status.HTTP_200_OK)
