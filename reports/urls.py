from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SustainabilityReportViewSet

router = DefaultRouter()
router.register(r'', SustainabilityReportViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
]