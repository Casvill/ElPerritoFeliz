# enrollments/views/matricula_views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from enrollments.serializers import MatriculaSerializer
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
                tamano=data.get('tamano', 'Mediano'),
                fecha_nacimiento=data['fecha_nacimiento'],
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

    def get(self, request):
        """
        Listar matrículas:
        - Si hay query param dueno_identificacion, filtra por ese dueño
        - Si solo_vigentes=true, filtra por matrículas activas (estado='Activa')
        """
        dueno_identificacion = request.query_params.get('dueno_identificacion')
        solo_vigentes = request.query_params.get('solo_vigentes') == 'true'

        # Si se pasó un documento de dueño, buscamos a ese usuario
        if dueno_identificacion:
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                dueno = User.objects.get(documento=dueno_identificacion)
            except User.DoesNotExist:
                return Response([], status=status.HTTP_200_OK)  # Retornamos lista vacía si no existe
            caninos = Canino.objects.filter(id_dueno=dueno)
        else:
            # Si no hay documento, devolvemos las mascotas del usuario autenticado
            caninos = Canino.objects.filter(id_dueno=request.user)

        matriculas = Matricula.objects.filter(id_canino__in=caninos)

        if solo_vigentes:
            matriculas = matriculas.filter(estado='Activa')

        serializer = MatriculaSerializer(matriculas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk=None):
        """
        Elimina una matrícula (y opcionalmente el canino asociado)
        """
        user = request.user
        matricula = get_object_or_404(Matricula, id_matricula=pk, id_canino__id_dueno=user)

        canino = matricula.id_canino
        matricula.delete()  # Esto elimina solo la matrícula
        # canino.delete()   # Descomenta si quieres eliminar también el canino

        # Intentamos eliminar el archivo en Supabase, pero no afectamos la respuesta
        try:
            from supabase import create_client
            supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_ANON_KEY'))
            if canino.carnet_vacunacion_url:
                file_name = canino.carnet_vacunacion_url.split('/')[-1]
                supabase.storage.from_('carnet_vacunacion').remove([file_name])
        except Exception as e:
            print('Error eliminando archivo en Supabase:', e)

        return Response({'mensaje': 'Matrícula eliminada correctamente.'}, status=status.HTTP_200_OK)
