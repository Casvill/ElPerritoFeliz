# ----------------------------------------------
# canines/models.py
# ----------------------------------------------
from django.db import models
from users.models import Usuario

class Canino(models.Model):
    TMINI = 'Mini'
    TPEQ = 'Pequeño'
    TMED = 'Mediano'
    TGRA = 'Grande'
    TAMANO_CHOICES = [
        (TMINI, 'Mini'),
        (TPEQ, 'Pequeño'),
        (TMED, 'Mediano'),
        (TGRA, 'Grande'),
    ]

    id_canino = models.BigAutoField(primary_key=True)
    id_dueno = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='caninos')
    nombre = models.CharField(max_length=150)
    raza = models.CharField(max_length=150, blank=True)
    tamano = models.CharField(max_length=20, choices=TAMANO_CHOICES, default=TMED)
    edad_meses = models.IntegerField(null=True, blank=True)
    carnet_vacunacion_url = models.TextField(blank=True)
    desparasitado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.raza})"
