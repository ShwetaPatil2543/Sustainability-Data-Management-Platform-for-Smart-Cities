from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AirQualityViewSet

router = DefaultRouter()
router.register(r'air-quality', AirQualityViewSet, basename='air-quality')

urlpatterns = [
    path('', include(router.urls)),  # This makes /air-quality/upload/ work
]