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
        user = request.user

        try:
            canino_id = data.get('id_canino')
            tipo_llegada = data.get('tipo_llegada')
            fecha = data.get('fecha')

            # Si no envían fecha → usar HOY
            if not fecha:
                fecha = timezone.localdate()

            if not canino_id or not tipo_llegada:
                return Response({'error': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

            # -----------------------------------------------------------------------
            # 🔍 1️⃣ VALIDAR: ¿Ya existe una asistencia hoy para este canino?
            # -----------------------------------------------------------------------
            asistencia_hoy = Asistencia.objects.filter(
                id_canino_id=canino_id,
                fecha=fecha
            ).first()

            if asistencia_hoy:
                return Response(
                    {"error": "Este canino ya tiene una asistencia registrada para este día."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # -----------------------------------------------------------------------
            # 🔍 2️⃣ VALIDAR: ¿Tiene una asistencia activa (sin salida)?
            # -----------------------------------------------------------------------
            asistencia_activa = Asistencia.objects.filter(
                id_canino_id=canino_id,
                salida__isnull=True
            ).first()

            if asistencia_activa:
                return Response(
                    {"error": "Este canino ya se encuentra en la escuela actualmente."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # -----------------------------------------------------------------------
            # 3️⃣ Crear asistencia normalmente
            # -----------------------------------------------------------------------
            canino = Canino.objects.get(id_canino=canino_id)

            asistencia = Asistencia.objects.create(
                id_canino=canino,
                tipo_llegada=tipo_llegada,
                fecha=fecha,
                registrado_por_id=request.user.id_usuario
            )

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
            # 1️⃣ Registrar salida
            # -------------------------------------------------------------
            asistencia.salida = timezone.localtime().time()
            asistencia.motivo_salida = motivo_salida or ""
            asistencia.quien_retiro = quien_retiro or ""
            asistencia.save()

            canino = asistencia.id_canino
            user = request.user

            # -------------------------------------------------------------
            # 2️⃣ REGISTRAR APRENDIZAJE Y CONDICIÓN FÍSICA
            # -------------------------------------------------------------
            if not salida_anticipada:

                hoy = timezone.localdate()
                mes = hoy.month
                anio = hoy.year

                # ---------------------------------------------------------
                # APRENDIZAJE (mensual)
                # Si ya existe registro del mes → actualizar
                # ---------------------------------------------------------
                aprendizaje, created = Aprendizaje.objects.get_or_create(
                    id_canino=canino,
                    mes=mes,
                    anio=anio,
                    defaults={
                        "obediencia": request.data.get("obediencia"),
                        "sociabilidad": request.data.get("sociabilidad"),
                        "conciencia": request.data.get("conciencia"),
                        "actividad": request.data.get("actividad"),
                        "estado_animo": request.data.get("animo"),
                        "registrado_por": user,
                    }
                )

                if not created:
                    # Ya existía → actualizar valores
                    aprendizaje.obediencia = request.data.get("obediencia")
                    aprendizaje.sociabilidad = request.data.get("sociabilidad")
                    aprendizaje.conciencia = request.data.get("conciencia")
                    aprendizaje.actividad = request.data.get("actividad")
                    aprendizaje.estado_animo = request.data.get("animo")
                    aprendizaje.save()

                # ---------------------------------------------------------
                # CONDICIÓN FÍSICA (diaria)
                # Si ya existe registro del día → actualizar
                # ---------------------------------------------------------
                condicion, created = CondicionFisica.objects.get_or_create(
                    id_canino=canino,
                    fecha=hoy,
                    defaults={
                        "peso": request.data.get("peso"),
                        "pelaje_piel": request.data.get("pelaje_piel"),
                        "color_mucosas": request.data.get("mucosas"),
                        "observaciones": request.data.get("abdomen", ""),
                        "registrado_por": user,
                    }
                )

                if not created:
                    condicion.peso = request.data.get("peso")
                    condicion.pelaje_piel = request.data.get("pelaje_piel")
                    condicion.color_mucosas = request.data.get("mucosas")
                    condicion.observaciones = request.data.get("abdomen", "")
                    condicion.save()

            # -------------------------------------------------------------
            # 3️⃣ Respuesta final
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



class EliminarAsistenciaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id_asistencia):
        try:
            asistencia = Asistencia.objects.get(id_asistencia=id_asistencia)

            # Si quieres validar que sólo el que creó la asistencia pueda borrarla:
            if asistencia.registrado_por_id != request.user.id_usuario:
                return Response(
                    {"error": "No tienes permiso para borrar esta asistencia."},
                    status=status.HTTP_403_FORBIDDEN
                )

            asistencia.delete()

            return Response(
                {"mensaje": "Asistencia eliminada correctamente."},
                status=status.HTTP_204_NO_CONTENT
            )

        except Asistencia.DoesNotExist:
            return Response(
                {"error": "Asistencia no encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print("❌ Error al eliminar asistencia:", e)
            return Response({"error": str(e)}, status=400)
