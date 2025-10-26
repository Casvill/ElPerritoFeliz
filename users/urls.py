#----------------------------------------------------------
# users/urls.py
#----------------------------------------------------------
from django.urls import path
from .views.login_views import LoginView, verify_recaptcha
from .views.register_views import check_documento, check_email, register_user

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('auth/verify-recaptcha/', verify_recaptcha, name='verify-recaptcha'),
    path('check-email/', check_email, name='check_email'),
    path('check-documento/', check_documento, name='check_documento'),
    path('register/', register_user, name='register_user'),
]
