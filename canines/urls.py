#----------------------------------------------
# Import necessary modules
#----------------------------------------------
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaninoViewSet


#----------------------------------------------
# Router configuration
#----------------------------------------------
router = DefaultRouter()
router.register(r'canines', CaninoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
