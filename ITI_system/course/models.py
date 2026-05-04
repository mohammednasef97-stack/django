from django.db import models

 
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_weeks = models.PositiveIntegerField()

    def __str__(self):
        return self.title
