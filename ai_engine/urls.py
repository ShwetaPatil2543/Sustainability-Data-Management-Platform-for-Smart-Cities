from django.urls import path
from .views import AIAdvisorView, AIRecommendationView, SustainabilityScoreView, PredictionsView

urlpatterns = [
    path("ai-advisor/", AIAdvisorView.as_view(), name="ai-advisor"),
    path("recommendations/", AIRecommendationView.as_view(), name="recommendations"),
    path("sustainability-score/", SustainabilityScoreView.as_view(), name="sustainability-score"),
    path("predictions/", PredictionsView.as_view(), name="predictions"),
]