from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from instructor import views as acc_views
from instructor.forms import StyledAuthenticationForm

urlpatterns = [
    path(
        "",
        login_required(TemplateView.as_view(template_name="home.html")),
        name="home",
    ),
    path("admin/", admin.site.urls),
    path("trainee/", include("trainee.urls")),
    path("course/", include("course.urls")),
    path("register/", acc_views.register, name="register"),
    path("instructor/", include("instructor.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            authentication_form=StyledAuthenticationForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
