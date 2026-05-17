from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CourseViewSet, TraineeViewSet

router = DefaultRouter()
router.register(r"trainees", TraineeViewSet, basename="api-trainee")
router.register(r"courses", CourseViewSet, basename="api-course")

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
