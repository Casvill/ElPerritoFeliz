# ----------------------------------------------
# api/urls.py
# ----------------------------------------------
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UsuarioViewSet

# Create router
router = DefaultRouter()

# Register viewsets
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path('', include(router.urls)),
]
