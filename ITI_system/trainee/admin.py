from django.contrib import admin

from .models import Trainee


@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "age", "join_date", "user")
    search_fields = ("name", "email")
    list_filter = ("join_date",)
