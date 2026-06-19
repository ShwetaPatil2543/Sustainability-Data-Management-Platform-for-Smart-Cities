# dashboard/urls.py
from django.urls import path
from .views import admin_dashboard, manager_dashboard, analyst_dashboard, DashboardStatsView, SmartDashboardView

urlpatterns = [
    path('admin/', admin_dashboard, name='admin-dashboard'),
    path('manager/', manager_dashboard, name='manager-dashboard'),
    path('analyst/', analyst_dashboard, name='analyst-dashboard'),
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('smart/', SmartDashboardView.as_view(), name='dashboard-smart'),
]