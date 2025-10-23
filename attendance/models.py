# ----------------------------------------------
# attendance/models.py
# ----------------------------------------------
from django.db import models
from canines.models import Canino
from users.models import Usuario

# ----------------------------------------------
# Attendance / Asistencia
# ----------------------------------------------
class Asistencia(models.Model):
    RUTA = 'Ruta'
    PROPIETARIO = 'Propietario'
    TIPO_LLEGADA_CHOICES = [
        (RUTA, 'Ruta'),
        (PROPIETARIO, 'Propietario'),
    ]

    id_asistencia = models.BigAutoField(primary_key=True)
    id_canino = models.ForeignKey(Canino, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField()
    llegada = models.TimeField("Hora de llegada",null=True, blank=True)
    salida = models.TimeField("Hora de salida", null=True, blank=True)
    motivo_salida = models.TextField("Motivo de salida", blank=True)
    quien_retiro = models.CharField("Quién retiró", max_length=200, blank=True)
    tipo_llegada = models.CharField("Tipo de llegada", max_length=20, choices=TIPO_LLEGADA_CHOICES)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='asistencias_registradas')

    def __str__(self):
        return f"Asistencia {self.id_asistencia} - {self.id_canino.nombre} on {self.fecha}"

# ----------------------------------------------
# Aprendizaje (monthly progress)
# ----------------------------------------------
class Aprendizaje(models.Model):
    id_aprendizaje = models.BigAutoField(primary_key=True)
    id_canino = models.ForeignKey(Canino, on_delete=models.CASCADE, related_name='aprendizajes')
    mes = models.IntegerField()
    anio = models.IntegerField()
    obediencia = models.SmallIntegerField()
    sociabilidad = models.SmallIntegerField()
    conciencia = models.SmallIntegerField()
    actividad = models.SmallIntegerField()
    estado_animo = models.SmallIntegerField()
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='aprendizajes_registrados')

    class Meta:
        unique_together = ('id_canino', 'mes', 'anio')  # one record per month-year

    def __str__(self):
        return f"Aprendizaje {self.id_canino.nombre} {self.mes}/{self.anio}"

# ----------------------------------------------
# Condición Física
# ----------------------------------------------
class CondicionFisica(models.Model):
    id_condicion = models.BigAutoField(primary_key=True)
    id_canino = models.ForeignKey(Canino, on_delete=models.CASCADE, related_name='condiciones')
    fecha = models.DateField()
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    pelaje_piel = models.CharField(max_length=255, blank=True)
    color_mucosas = models.CharField(max_length=255, blank=True)
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='condiciones_registradas')

    class Meta:
        verbose_name = 'Condición física'
        verbose_name_plural = 'Condición física'

    def __str__(self):
        return f"Condición {self.id_canino.nombre} en {self.fecha}"
