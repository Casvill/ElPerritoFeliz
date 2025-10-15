# ----------------------------------------------
# attendance/serializers.py
# ----------------------------------------------
from rest_framework import serializers
from .models import Asistencia, Aprendizaje, CondicionFisica

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'

class AprendizajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aprendizaje
        fields = '__all__'

class CondicionFisicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicionFisica
        fields = '__all__'
