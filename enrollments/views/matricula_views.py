from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Canino, Matricula
from users.models import Usuario
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import date, datetime, timedelta
from django.conf import settings
import os


class RegistrarMatriculaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user  # usuario autenticado por JWT

        try:
            # ✅ 1️⃣ Crear o registrar el canino
            canino = Canino.objects.create(
                id_dueno=user,
                nombre=data['nombre'],
                raza=data.get('raza', ''),
                tamano=data.get('talla', 'Mediano'),
                edad_meses=self._calcular_edad_meses(data['nacimiento']),
                carnet_vacunacion_url=data.get('vacunas_url', ''),
            )

            # ✅ 2️⃣ Calcular fechas de matrícula
            fecha_inicio = date.today()
            plan = data['plan']

            if plan == 'mensual':
                fecha_fin = fecha_inicio + timedelta(days=30)
            elif plan == 'bimestre':
                fecha_fin = fecha_inicio + timedelta(days=60)
            elif plan == 'trimestre':
                fecha_fin = fecha_inicio + timedelta(days=90)
            elif plan == 'medio_año':
                fecha_fin = fecha_inicio + timedelta(days=180)
            else:
                fecha_fin = fecha_inicio + timedelta(days=365)

            # ✅ 3️⃣ Obtener precio desde .env o usar valores por defecto
            plan_precios = {
                'mensual': float(os.getenv('PRECIO_PLAN_1M', 100000)),
                'bimestre': float(os.getenv('PRECIO_PLAN_2B', 180000)),
                'trimestre': float(os.getenv('PRECIO_PLAN_3T', 250000)),
                'medio_año': float(os.getenv('PRECIO_PLAN_6M', 450000)),
                'año': float(os.getenv('PRECIO_PLAN_1Y', 800000)),
            }
            precio = plan_precios.get(plan, 100000)

            # ✅ 4️⃣ Crear la matrícula
            matricula = Matricula.objects.create(
                id_canino=canino,
                plan=plan,
                transporte=data['transporte'],
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado=Matricula.EST_ACTIVA,
                precio=precio,
            )

            return Response({
                'mensaje': '✅ Matrícula registrada correctamente',
                'canino_id': canino.id_canino,
                'matricula_id': matricula.id_matricula,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("❌ Error registrando matrícula:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def _calcular_edad_meses(self, nacimiento):
        nacimiento = datetime.strptime(nacimiento, "%Y-%m-%d").date()
        today = date.today()
        return (today.year - nacimiento.year) * 12 + today.month - nacimiento.month
