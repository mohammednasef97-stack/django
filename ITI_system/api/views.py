from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from course.models import Course
from trainee.models import Trainee

from .serializers import CourseSerializer, TraineeSerializer


class TraineeViewSet(viewsets.ModelViewSet):
    serializer_class = TraineeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trainee.objects.filter(is_deleted=False).order_by("-join_date", "name")

    def perform_destroy(self, instance):
        instance.soft_delete()


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(is_deleted=False).order_by("title")

    def perform_destroy(self, instance):
        instance.soft_delete()
