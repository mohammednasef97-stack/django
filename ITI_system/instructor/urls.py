from django.urls import path

from . import views

app_name = "instructor"
urlpatterns = [
    path("", views.instructor_list, name="instructor_home"),
    path("list/", views.instructor_list, name="instructor_list"),
    path("add/", views.add_instructor, name="add_instructor"),
    path("update/<int:id>/", views.update_instructor, name="update_instructor"),
    path("delete/<int:id>/", views.delete_instructor, name="delete_instructor"),
    path("<int:id>/", views.instructor_detail, name="instructor_detail"),
]
