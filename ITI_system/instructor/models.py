from django.db import models

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    salary = models.FloatField()

    def __str__(self):
        return self.name