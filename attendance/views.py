# attendance/views.py
from datetime import datetime, time
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Aprendizaje, Asistencia, Canino, CondicionFisica
from django.utils import timezone

class RegistrarAsistenciaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user  # <-- Usuario autenticado

        try:
            canino_id = data.get('id_canino')
            tipo_llegada = data.get('tipo_llegada')
            fecha = data.get('fecha')
            if not fecha:
                fecha = timezone.localdate()

            if not canino_id or not tipo_llegada:
                return Response({'error': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

            canino = Canino.objects.get(id_canino=canino_id)

            asistencia = Asistencia.objects.create(
                id_canino=canino,
                tipo_llegada=tipo_llegada,
                fecha=fecha,
                registrado_por_id=request.user.id_usuario  # <-- Aquí guardamos quién registró
            )
            print("Fecha que se enviará a Supabase:", fecha)
            return Response({
                'mensaje': 'Asistencia registrada correctamente',
                'asistencia_id': asistencia.id_asistencia
            }, status=status.HTTP_201_CREATED)

        except Canino.DoesNotExist:
            return Response({'error': 'Canino no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ListarAsistenciasView(APIView):
    """
    Lista todas las asistencias registradas por el usuario autenticado,
    ignorando fecha. Puede filtrar solo presentes con ?solo_presentes=true
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # 🔹 Traer todos los caninos que tiene el usuario logueado
            caninos = Canino.objects.filter(id_dueno_id=request.user.id_usuario)

            print("Usuario logueado:", request.user, request.user.id_usuario)
            # 🔹 Traer todas las asistencias registradas por el usuario
            asistencias = Asistencia.objects.filter(
                registrado_por_id=request.user.id_usuario,
            )


            # 🔹 Filtrado opcional: solo presentes
            solo_presentes = request.query_params.get('solo_presentes')
            if solo_presentes and solo_presentes.lower() == 'true':
                asistencias = asistencias.filter(salida__isnull=True)


            # 🔹 DEBUG: imprime qué asistencias encontró
            print("Asistencias del usuario logueado:", list(asistencias.values('id_canino__nombre','fecha','tipo_llegada')))

            # 🔹 Preparar datos para el frontend
            data = [
                {
                    "id": a.id_asistencia,
                    "canino_nombre": a.id_canino.nombre,
                    "llego_ruta": a.tipo_llegada == 'Ruta',
                    "llego_duenio": a.tipo_llegada == 'Propietario',
                    "hora_ingreso": a.llegada.strftime('%H:%M') if a.llegada else None,
                    "registrado_por": f"{a.registrado_por.nombres} {a.registrado_por.apellidos}" if a.registrado_por else None,
                }
                for a in asistencias
            ]

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class RegistrarSalidaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            asistencia_id = request.data.get("id_asistencia")
            motivo_salida = request.data.get("motivo_salida", "")
            quien_retiro = request.data.get("quien_retiro", "")
            salida_anticipada = request.data.get("salida_anticipada", False)

            if not asistencia_id or not quien_retiro:
                return Response({"error": "Faltan datos requeridos"}, status=400)


            asistencia = Asistencia.objects.get(id_asistencia=asistencia_id)

            # -------------------------------------------------------------
            # 1️⃣  Registrar salida normalmente
            # -------------------------------------------------------------
            asistencia.salida = timezone.localtime().time()
            asistencia.motivo_salida = motivo_salida or ""
            asistencia.quien_retiro = quien_retiro or ""
            asistencia.save()

            canino = asistencia.id_canino
            user = request.user

            # -------------------------------------------------------------
            # 2️⃣  SI NO ES SALIDA ANTICIPADA → REGISTRAR APRENDIZAJE Y SALUD
            # -------------------------------------------------------------
            if not salida_anticipada:
                # Datos de aprendizaje
                Aprendizaje.objects.create(
                    id_canino=canino,
                    mes=timezone.localdate().month,
                    anio=timezone.localdate().year,
                    obediencia=request.data.get("obediencia"),
                    sociabilidad=request.data.get("sociabilidad"),
                    conciencia=request.data.get("conciencia"),
                    actividad=request.data.get("actividad"),
                    estado_animo=request.data.get("animo"),
                    registrado_por=user
                )

                # Datos de condición física
                CondicionFisica.objects.create(
                    id_canino=canino,
                    fecha=timezone.localdate(),
                    peso=request.data.get("peso"),
                    pelaje_piel=request.data.get("pelaje_piel"),
                    color_mucosas=request.data.get("mucosas"),
                    observaciones=request.data.get("abdomen", ""),
                    registrado_por=user
                )

            # -------------------------------------------------------------
            # 3️⃣ Respuesta
            # -------------------------------------------------------------
            return Response({
                "mensaje": "Salida registrada correctamente",
                "id_asistencia": asistencia.id_asistencia,
                "hora_salida": asistencia.salida.strftime('%H:%M'),
                "salida_anticipada": salida_anticipada
            }, status=200)

        except Asistencia.DoesNotExist:
            return Response({"error": "Asistencia no encontrada"}, status=404)
        except Exception as e:
            print("❌ Error registrar salida:", e)
            return Response({"error": str(e)}, status=400)
