# ----------------------------------------------
# ElPerritoFeliz/urls.py
# ----------------------------------------------
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import home
from users.views.login_views import UsuarioViewSet, CustomValidateTokenView
from dashboard.views.client_dashboard_views import ClienteDashboardView

# ----------------------------------------------
# Create DRF router and register endpoints
# ----------------------------------------------
router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')

# ----------------------------------------------
# URL patterns
# ----------------------------------------------
urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('users.urls')),
    path('api/password_reset/validate_token/',CustomValidateTokenView.as_view(),name='password_reset_validate_token',),
    path('api/password_reset/',include('django_rest_passwordreset.urls', namespace='password_reset'),),
    path('api/', include('enrollments.urls')),
    path("api/dashboard/", include("dashboard.urls")),

]

# ----------------------------------------------
# Optional: API root for DRF
# ----------------------------------------------
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
