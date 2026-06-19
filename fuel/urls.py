from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FuelConsumptionViewSet, FuelUploadView

router = DefaultRouter()
router.register(r'fuel', FuelConsumptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', FuelUploadView.as_view()),
]