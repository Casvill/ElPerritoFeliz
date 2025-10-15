# ----------------------------------------------
# ElPerritoFeliz/urls.py
# ----------------------------------------------
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import home  # 👈 importa la vista

# Importa los viewsets de tus apps
from users.views import UsuarioViewSet       # ejemplo para CRUD usuarios
from clients.views import ClientViewSet      # módulo gestión de clientes

# ----------------------------------------------
# Create DRF router and register endpoints
# ----------------------------------------------
router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
# Nota: no registramos ClientViewSet aquí porque tiene rutas personalizadas
# que vienen desde clients/urls.py

# ----------------------------------------------
# URL patterns
# ----------------------------------------------
urlpatterns = [
    path('', home),  # 👈 ruta raíz
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # o donde tengas tus endpoints principales
]

# ----------------------------------------------
# Optional: API root for DRF
# ----------------------------------------------
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
