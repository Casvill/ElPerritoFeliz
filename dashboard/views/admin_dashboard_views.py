# ----------------------------------------------
# dashboard/views/admin_dashboard_views.py
# ----------------------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import date, datetime, timedelta
from django.db.models import Count, Sum, Q
from enrollments.models import Matricula
from users.models import Usuario
from canines.models import Canino


# ----------------------------------------------
# Vista Dashboard para Admin / Director
# ----------------------------------------------
class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hoy = date.today()
        mes_inicio = hoy.replace(day=1)
        mes_fin = (mes_inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # === KPI 1: Perros matriculados este mes ===
        matriculas_mes = Matricula.objects.filter(
            fecha_inicio__range=[mes_inicio, mes_fin]
        ).count()

        # === KPI 2: Entrenadores activos ===
        entrenadores_activos = Usuario.objects.filter(
            tipo_usuario="ENTRENADOR", is_active=True
        ).count()

        # === KPI 3: Ingresos del mes (suma de precios) ===
        ingresos_mes = (
            Matricula.objects.filter(
                fecha_inicio__range=[mes_inicio, mes_fin]
            ).aggregate(total=Sum("precio"))["total"]
            or 0
        )

        # === KPI 4: Asistencia promedio ===
        # 🔸 Por ahora se simula, luego puede venir de modelo Asistencia
        asistencia_pct = 85

        # === Distribución de transporte ===
        transporte = Matricula.objects.filter(fecha_inicio__range=[mes_inicio, mes_fin])
        transporte_data = {
            "total": transporte.filter(transporte="Total").count(),
            "parcial": transporte.filter(transporte="Parcial").count(),
            "sin": transporte.filter(transporte="Ninguno").count(),
        }

        # === Distribución de planes ===
        plan_data = {
            "mensual": transporte.filter(plan="1 mes").count(),
            "bimestral": transporte.filter(plan="1 bimestre").count(),
            "trimestral": transporte.filter(plan="1 trimestre").count(),
            "semestral": transporte.filter(plan="1 semestre").count(),
            "anual": transporte.filter(plan="1 año").count(),
        }

        # === Serie últimos 6 meses ===
        serie6 = []
        for i in range(5, -1, -1):
            d = (mes_inicio - timedelta(days=30 * i)).replace(day=1)
            inicio = d
            fin = (inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            count = Matricula.objects.filter(
                fecha_inicio__range=[inicio, fin]
            ).count()
            serie6.append({
                "key": f"{inicio.year}-{inicio.month:02d}",
                "label": f"{inicio.strftime('%b')} {str(inicio.year)[2:]}",
                "value": count,
            })

        # === Últimas matrículas ===
        ultimas = Matricula.objects.select_related("id_canino", "id_canino__id_dueno").order_by("-fecha_creacion")[:5]
        ultimas_data = [
            {
                "name": m.id_canino.nombre,
                "owner": f"{m.id_canino.id_dueno.first_name} {m.id_canino.id_dueno.last_name}",
                "plan": m.plan,
                "edad": f"{m.id_canino.edad_meses // 12} años",
                "fecha": m.fecha_inicio.strftime("%d %b, %Y"),
                "avatar": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
            }
            for m in ultimas
        ]

        data = {
            "kpiMatriculadosMes": matriculas_mes,
            "kpiEntrenadoresActivos": entrenadores_activos,
            "kpiIngresosMes": ingresos_mes,
            "kpiAsistenciaPct": asistencia_pct,
            "transporteMes": transporte_data,
            "planesMes": plan_data,
            "serie6": serie6,
            "ultimasMatriculas": ultimas_data,
        }

        return Response(data, status=status.HTTP_200_OK)
