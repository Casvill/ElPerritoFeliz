# users/views/clientes_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Count
from users.models import Usuario
from rest_framework import status


class ListadoGlobalClientesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # 🔹 SOLO clientes
            queryset = Usuario.objects.filter(tipo_usuario="CLIENTE").annotate(
                cantidad_mascotas=Count('caninos')
            )

            # ===== FILTROS =====
            estado = request.query_params.get("estado")
            fecha_desde = request.query_params.get("fechaDesde")
            fecha_hasta = request.query_params.get("fechaHasta")

            if estado:
                queryset = queryset.filter(activo=(estado == "ACTIVO"))

            if fecha_desde:
                queryset = queryset.filter(fecha_registro__date__gte=fecha_desde)

            if fecha_hasta:
                queryset = queryset.filter(fecha_registro__date__lte=fecha_hasta)

            # ===== SERIALIZACIÓN MANUAL =====
            data = [
                {
                    "id": u.id_usuario,
                    "nombre": u.nombres,
                    "apellido": u.apellidos,
                    "tipoDocumento": u.tipo_documento,
                    "numeroDocumento": u.documento,
                    "email": u.email,
                    "telefono": u.telefono,
                    "estado": "ACTIVO" if u.activo else "INACTIVO",
                    "fechaRegistro": u.fecha_registro,
                    "cantidadMascotas": u.cantidad_mascotas,
                }
                for u in queryset
            ]

            return Response(data, status=200)

        except Exception as e:
            print("❌ Error listado global clientes:", e)
            return Response({"error": str(e)}, status=400)
