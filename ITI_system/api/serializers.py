from rest_framework import serializers

from course.models import Course
from trainee.models import Trainee


class TraineeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainee
        fields = (
            "id",
            "name",
            "email",
            "age",
            "join_date",
            "photo",
        )
        read_only_fields = ("id", "join_date")


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "duration_weeks",
            "cover_image",
        )
        read_only_fields = ("id",)
