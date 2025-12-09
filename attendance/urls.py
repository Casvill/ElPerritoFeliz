# attendance/urls.py
from django.urls import path
from .views import EliminarAsistenciaView, RegistrarAsistenciaView, ListarAsistenciasView, RegistrarSalidaView

urlpatterns = [
    path('asistencias/', RegistrarAsistenciaView.as_view(), name='asistencias-list'),
    path('asistencias/listar/', ListarAsistenciasView.as_view(), name='listar_asistencias'),
    path('asistencias/registrar-salida/', RegistrarSalidaView.as_view(), name='registrar_salida'),
    path('asistencias/<int:id_asistencia>/', EliminarAsistenciaView.as_view()),
]
