from django.contrib.auth import views as django_auth_views
from django.urls import path

app_name = "users"

urlpatterns = [
    path(
        "login/",
        django_auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login"
    ),
    path(
        "logout/",
        django_auth_views.LogoutView.as_view(
            template_name="users/logout.html"),
        name="logout"
    ),
    # path("signup/", , name="signup"),
]