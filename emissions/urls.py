from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CarbonEmissionViewSet,
    bulk_upload_emissions,
    industry_list,
    get_departments,
    bulk_upload_status,
    aggregates,
    trends,
    top_emitters,
    dashboard_summary,
)
router = DefaultRouter()
router.register(r'', CarbonEmissionViewSet) # router handles /api/emissions/

urlpatterns = [

    path("industries/", industry_list, name="industries"),
    path("industries/<int:industry_id>/departments/", get_departments, name="industry_departments"),
    path("bulk-upload/", bulk_upload_emissions),
    path("bulk-upload/status/<int:audit_id>/", bulk_upload_status, name="emissions_bulk_status"),
    path("aggregates/", aggregates, name="emissions_aggregates"),
    path("trends/", trends, name="emissions_trends"),
    path("top-emitters/", top_emitters, name="emissions_top_emitters"),
    path("dashboard-summary/", dashboard_summary, name="emissions_dashboard_summary"),
    path("", include(router.urls)),  # router last
]