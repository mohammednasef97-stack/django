from django.contrib import admin
from django.urls import path, include
from instructor import views as acc_views
from trainee import views as trainee_views
from course import views as course_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trainee/', include('trainee.urls')),
    path('course/', include('course.urls')),
    path('register/', acc_views.register, name='register'),
    path('instructor/',include('instructor.urls')),
    path('login/', acc_views.login_view, name='login'),
]

 