# ----------------------------------------------
# enrollments/models.py
# ----------------------------------------------
from django.db import models
from canines.models import Canino  # 👈 importa el modelo Canino

# ----------------------------------------------
# Enrollment / Matricula
# ----------------------------------------------
class Matricula(models.Model):
    PLAN_1M = '1 mes'
    PLAN_2B = '1 bimestre'
    PLAN_3T = '1 trimestre'
    PLAN_6M = '1 semestre'
    PLAN_1Y = '1 año'
    PLAN_CHOICES = [
        (PLAN_1M, '1 mes'),
        (PLAN_2B, '1 bimestre'),
        (PLAN_3T, '1 trimestre'),
        (PLAN_6M, '1 semestre'),
        (PLAN_1Y, '1 año'),
    ]

    TRANSPORTE_TOTAL = 'Total'
    TRANSPORTE_PARCIAL = 'Parcial'
    TRANSPORTE_NINGUNO = 'Ninguno'
    TRANSPORTE_CHOICES = [
        (TRANSPORTE_TOTAL, 'Total'),
        (TRANSPORTE_PARCIAL, 'Parcial'),
        (TRANSPORTE_NINGUNO, 'Ninguno'),
    ]

    EST_ACTIVA = 'Activa'
    EST_PROX = 'Próxima a vencer'
    EST_VENC = 'Vencida'
    ESTADO_CHOICES = [
        (EST_ACTIVA, 'Activa'),
        (EST_PROX, 'Próxima a vencer'),
        (EST_VENC, 'Vencida'),
    ]

    id_matricula = models.BigAutoField(primary_key=True)

    # 🔗 Relación con Canino
    id_canino = models.ForeignKey(Canino, on_delete=models.CASCADE, related_name='matriculas', null=True, blank=True)

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    transporte = models.CharField(max_length=20, choices=TRANSPORTE_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default=EST_ACTIVA)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Matricula {self.id_matricula} - {self.id_canino.nombre} ({self.plan})"
