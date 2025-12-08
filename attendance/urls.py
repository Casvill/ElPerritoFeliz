# attendance/urls.py
from django.urls import path
from .views import RegistrarAsistenciaView, ListarAsistenciasView

urlpatterns = [
    path('asistencias/', RegistrarAsistenciaView.as_view(), name='asistencias-list'),
     path('asistencias/listar/', ListarAsistenciasView.as_view(), name='listar_asistencias'),
]
