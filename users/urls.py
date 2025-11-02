# ----------------------------------------------------------
# users/urls.py
# ----------------------------------------------------------
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.login_views import LoginView, verify_recaptcha
from .views.register_views import check_documento, check_email, register_user
from .views.internaluser_views import UsuarioInternoViewSet
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

# Router para viewsets (usuarios internos)
router = DefaultRouter()
router.register(r'usuarios-internos', UsuarioInternoViewSet, basename='usuarios-internos')

urlpatterns = [
    # --- Rutas existentes ---
    path('login/', LoginView.as_view(), name='login'),
    path('auth/verify-recaptcha/', verify_recaptcha, name='verify-recaptcha'),
    path('check-email/', check_email, name='check_email'),
    path('check-documento/', check_documento, name='check_documento'),
    path('register/', register_user, name='register_user'),

    # --- Nuevas rutas automáticas ---
    path('', include(router.urls)),

    # 🔹 JWT Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]