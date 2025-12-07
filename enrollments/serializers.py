# ----------------------------------------------
# enrollments/serializers.py
# ----------------------------------------------
from datetime import date
from rest_framework import serializers
from .models import Matricula

class MatriculaSerializer(serializers.ModelSerializer):
    # Datos del canino
    nombre = serializers.CharField(source='id_canino.nombre', read_only=True)
    raza = serializers.CharField(source='id_canino.raza', read_only=True)
    talla = serializers.CharField(source='id_canino.tamano', read_only=True)
    fecha_nacimiento = serializers.DateField(source='id_canino.fecha_nacimiento', read_only=True)
    vacunas_url = serializers.CharField(source='id_canino.carnet_vacunacion_url', read_only=True)

    edad_meses = serializers.SerializerMethodField()


    class Meta:
        model = Matricula
        fields = [
            'id_matricula',
            'plan',
            'transporte',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'precio',

            # Campos del canino 
            'nombre',
            'raza',
            'talla',
            'fecha_nacimiento',
            'edad_meses',
            'vacunas_url',
        ]

    def get_dueno_nombre(self, obj):
        # 🔹 Aseguramos acceso al dueño real del canino
        dueno = getattr(obj.id_canino, "id_dueno", None)
        if dueno:
            nombres = getattr(dueno, "nombres", "")
            apellidos = getattr(dueno, "apellidos", "")
            full_name = f"{nombres} {apellidos}".strip()
            return full_name if full_name else None
        return None

      # 🔹 Método que calcula edad en meses
    def get_edad_meses(self, obj):
        if obj.id_canino and obj.id_canino.fecha_nacimiento:
            nacimiento = obj.id_canino.fecha_nacimiento
            today = date.today()
            return (today.year - nacimiento.year) * 12 + today.month - nacimiento.month
        return None