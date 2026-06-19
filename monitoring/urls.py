from rest_framework.routers import DefaultRouter
from .views import AQIRecordViewSet, CarbonEmissionViewSet

router = DefaultRouter()
router.register(r'aqi', AQIRecordViewSet, basename='aqi')
router.register(r'emissions', CarbonEmissionViewSet, basename='emissions')

urlpatterns = router.urls
