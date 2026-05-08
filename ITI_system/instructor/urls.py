from django.urls import path
from . import views

urlpatterns = [

    path(
        'list/',
        views.instructorList
    ),

    path(
        'add/',
        views.addInstructor
    ),

    path(
        'delete/<int:id>',
        views.deleteInstructor
    ),
    path(
        'register/',
        views.register,
        name='register'
    ),
]