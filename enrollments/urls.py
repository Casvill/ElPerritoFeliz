# enrollments/urls.py
from django.urls import path
from .views.matricula_views import RegistrarMatriculaView

urlpatterns = [
    path('matriculas/', RegistrarMatriculaView.as_view(), name='registrar_matricula'),
]
