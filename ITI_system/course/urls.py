from django.urls import path

from . import views

app_name = "course"
urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("add/", views.add_course, name="add_course"),
    path("update/<int:id>/", views.update_course, name="update_course"),
    path("delete/<int:id>/", views.delete_course, name="delete_course"),
    path("<int:id>/", views.course_detail, name="course_detail"),
]
