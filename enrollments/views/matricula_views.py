# enrollments/views/matricula_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Canino, Matricula
from datetime import date, timedelta
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import os


class RegistrarMatriculaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user

        try:
            # 1️⃣ Crear el canino asociado al usuario
            canino = Canino.objects.create(
                id_dueno=user,
                nombre=data['nombre'],
                raza=data.get('raza', ''),
                tamano=data.get('talla', 'Mediano'),
                edad_meses=self._calcular_edad_meses(data['nacimiento']),
                carnet_vacunacion_url=data.get('vacunas_url', ''),
            )

            # 2️⃣ Calcular fechas según el plan
            fecha_inicio = date.today()
            plan = data['plan']
            duraciones = {
                'mensual': 30,
                'bimestre': 60,
                'trimestre': 90,
                'medio_año': 180,
                'año': 365,
            }
            dias = duraciones.get(plan, 30)
            fecha_fin = fecha_inicio + timedelta(days=dias)

            # 3️⃣ Determinar precio desde variables de entorno o valores por defecto
            plan_precios = {
                'mensual': int(os.getenv('PRECIO_PLAN_1M', 100000)),
                'bimestre': int(os.getenv('PRECIO_PLAN_2B', 180000)),
                'trimestre': int(os.getenv('PRECIO_PLAN_3T', 250000)),
                'medio_año': int(os.getenv('PRECIO_PLAN_6M', 450000)),
                'año': int(os.getenv('PRECIO_PLAN_1Y', 800000)),
            }
            precio = plan_precios.get(plan, 100000)

            # 4️⃣ Crear la matrícula con precio correcto
            matricula = Matricula.objects.create(
                id_canino=canino,
                plan=plan,
                transporte=data['transporte'],
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado='Activa',
                precio=precio,
            )

            return Response({
                'mensaje': 'Matrícula registrada correctamente',
                'canino_id': canino.id_canino,
                'matricula_id': matricula.id_matricula,
                'precio': precio,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("❌ Error registrando matrícula:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def _calcular_edad_meses(self, nacimiento):
        from datetime import datetime
        nacimiento = datetime.strptime(nacimiento, "%Y-%m-%d").date()
        today = date.today()
        return (today.year - nacimiento.year) * 12 + today.month - nacimiento.month
