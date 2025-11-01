# ----------------------------------------------
# ElPerritoFeliz/urls.py
# ----------------------------------------------
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import home  # 👈 importa la vista

# Importa los viewsets de tus apps
from users.views.login_views import UsuarioViewSet, CustomValidateTokenView


# ----------------------------------------------
# Create DRF router and register endpoints
# ----------------------------------------------
router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')


# ----------------------------------------------
# URL patterns
# ----------------------------------------------
urlpatterns = [
    path('', home),  # 👈 ruta raíz
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  
    path('api/', include('users.urls')),
    path('api/password_reset/validate_token/',CustomValidateTokenView.as_view(),name='password_reset_validate_token'),
    path('api/password_reset/',include('django_rest_passwordreset.urls', namespace='password_reset')),
]

# ----------------------------------------------
# Optional: API root for DRF
# ----------------------------------------------
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
