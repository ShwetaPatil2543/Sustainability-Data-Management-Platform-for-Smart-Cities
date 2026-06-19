from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CurrentUserView, LogoutView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

urlpatterns += router.urls