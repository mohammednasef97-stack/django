from django.conf import settings
from django.db import models
from django.utils import timezone


class Instructor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="instructor_profile",
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    salary = models.FloatField()
    photo = models.ImageField(
        upload_to="instructors/photos/", blank=True, null=True
    )
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])
