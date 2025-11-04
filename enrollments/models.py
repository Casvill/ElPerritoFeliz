# ----------------------------------------------
# enrollments/models.py
# ----------------------------------------------
from django.db import models
from canines.models import Canino 
from datetime import date, timedelta
import os

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

    def save(self, *args, **kwargs):

        # 🔹 Calcular fecha_fin según el plan
        if not self.fecha_fin:
            if self.plan == self.PLAN_1M:
                self.fecha_fin = date.today() + timedelta(days=30)
            elif self.plan == self.PLAN_2B:
                self.fecha_fin = date.today() + timedelta(days=60)
            elif self.plan == self.PLAN_3T:
                self.fecha_fin = date.today() + timedelta(days=90)
            elif self.plan == self.PLAN_6M:
                self.fecha_fin = date.today() + timedelta(days=180)
            elif self.plan == self.PLAN_1Y:
                self.fecha_fin = date.today() + timedelta(days=365)

        # 🔹 Precios base de los planes (puedes moverlos al .env si quieres)
        precios_plan = {
            self.PLAN_1M: float(os.getenv('PRECIO_PLAN_1M', 100000)),
            self.PLAN_2B: float(os.getenv('PRECIO_PLAN_2B', 180000)),
            self.PLAN_3T: float(os.getenv('PRECIO_PLAN_3T', 250000)),
            self.PLAN_6M: float(os.getenv('PRECIO_PLAN_6M', 450000)),
            self.PLAN_1Y: float(os.getenv('PRECIO_PLAN_1Y', 800000)),
        }

        # 🔹 Precios adicionales por transporte
        precios_transporte = {
            self.TRANSPORTE_TOTAL: float(os.getenv('PRECIO_TRANSPORTE_TOTAL', 80000)),
            self.TRANSPORTE_PARCIAL: float(os.getenv('PRECIO_TRANSPORTE_PARCIAL', 40000)),
            self.TRANSPORTE_NINGUNO: 0.0,
        }

        # 🔹 Calcular precio total
        precio_plan = precios_plan.get(self.plan, 0)
        precio_transporte = precios_transporte.get(self.transporte, 0)
        self.precio = precio_plan + precio_transporte

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Matricula {self.id_matricula} - {self.id_canino.nombre} ({self.plan})"
