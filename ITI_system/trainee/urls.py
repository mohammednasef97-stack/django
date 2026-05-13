from django.urls import path

from . import views

app_name = "trainee"
urlpatterns = [
    path("", views.trainee_list, name="trainee_list"),
    path("add/", views.add_trainee_fbv, name="add_trainee"),
    path(
        "add/create-view/",
        views.TraineeGenericCreateView.as_view(),
        name="add_trainee_createview",
    ),
    path(
        "add/cbv-manual/",
        views.TraineeManualInsertCBV.as_view(),
        name="add_trainee_cbv_manual",
    ),
    path("update/<int:id>/", views.update_trainee, name="update_trainee"),
    path("delete/<int:id>/", views.delete_trainee, name="delete_trainee"),
    path("<int:id>/", views.trainee_detail, name="trainee_detail"),
]
