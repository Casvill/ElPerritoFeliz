from django.contrib import admin
from attendance.models import Aprendizaje,Asistencia,CondicionFisica

# Register your models here.
admin.site.register(Aprendizaje)
admin.site.register(Asistencia)
admin.site.register(CondicionFisica)
