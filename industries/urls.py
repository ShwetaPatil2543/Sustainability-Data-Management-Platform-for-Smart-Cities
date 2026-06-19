from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndustryViewSet, DepartmentViewSet

router = DefaultRouter()

router.register(r'', IndustryViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]