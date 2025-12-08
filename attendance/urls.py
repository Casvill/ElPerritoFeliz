# attendance/urls.py
from django.urls import path
from .views import AsistenciasView

urlpatterns = [
    path('asistencias/', AsistenciasView.as_view(), name='asistencias-list'),
]
