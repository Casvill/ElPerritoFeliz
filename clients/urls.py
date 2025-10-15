# ----------------------------------------------
# clients/urls.py
# ----------------------------------------------
from django.urls import path
from .views import ClientViewSet

client_view = ClientViewSet.as_view({
    'post': 'register'
})

profile_view = ClientViewSet.as_view({
    'get': 'profile',
    'put': 'profile'
})

urlpatterns = [
    path('register/', client_view, name='client-register'),
    path('profile/<str:pk>/', profile_view, name='client-profile'),
]
