# enrollments/urls.py

from django.urls import path
from .views.matricula_views import RegistrarMatriculaView

urlpatterns = [
    path('matriculas/', RegistrarMatriculaView.as_view()),          # GET y POST
    path('matriculas/<int:pk>/', RegistrarMatriculaView.as_view()), # PUT y DELETE
]
