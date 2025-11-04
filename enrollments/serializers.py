# ----------------------------------------------
# enrollments/serializers.py
# ----------------------------------------------
from rest_framework import serializers
from .models import Matricula

class MatriculaSerializer(serializers.ModelSerializer):
    canino_nombre = serializers.CharField(source='id_canino.nombre', read_only=True)
    canino_raza = serializers.CharField(source='id_canino.raza', read_only=True)
    dueno_nombre = serializers.SerializerMethodField()

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
            'canino_nombre',
            'canino_raza',
            'dueno_nombre',
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
