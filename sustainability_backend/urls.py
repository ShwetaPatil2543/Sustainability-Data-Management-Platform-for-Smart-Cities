# sustainability_backend/urls.py

from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from ai_engine.views import AIAdvisorView

urlpatterns = [

    path('admin/', admin.site.urls),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # AI Advisor endpoint
    path('api/ai-advisor/', AIAdvisorView.as_view(), name='ai-advisor'),

    # Apps
    path('api/industries/', include('industries.urls')),
    path('api/emissions/', include('emissions.urls')),
    path('api/energy/', include('energy.urls')),
    path('api/fuel/', include('fuel.urls')),
    path('api/fuel-monitoring/', include('fuel.urls')),

    path('api/air-quality/', include('air_quality.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/ai/', include('ai_engine.urls')),
    path('api/users/', include('users.urls')),
    path('api/auth/', include('users.urls')),
    # Monitoring
    path('api/monitoring/', include('monitoring.urls')),
    path('api/workflow/', include('workflow.urls')),


]