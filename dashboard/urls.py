from django.urls import path
from dashboard.views.admin_dashboard_views import AdminDashboardView
from dashboard.views.client_dashboard_views import ClienteDashboardView

urlpatterns = [
    path("cliente/", ClienteDashboardView.as_view(), name="dashboard_cliente"),
    path("admin/", AdminDashboardView.as_view(), name="dashboard_admin"),
]
