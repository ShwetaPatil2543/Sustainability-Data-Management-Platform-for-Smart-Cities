from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnergyUsageViewSet, EnergyUploadView

router = DefaultRouter()
router.register(r"", EnergyUsageViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("upload/", EnergyUploadView.as_view(), name="energy-upload"),
]