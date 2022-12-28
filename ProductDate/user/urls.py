from django.urls import include, path
from rest_framework.authtoken import views

from .views import (
    ChangePasswordView,
    UserCreateAPIView,
    UserUpdateAPIView,
    delete_users,
)

urlpatterns = [
    path("api-token-auth/", views.obtain_auth_token),
    path("user_create/", UserCreateAPIView.as_view()),
    path("user_update/", UserUpdateAPIView.as_view()),
    path("change_password/", ChangePasswordView.as_view()),
    path("delete_users/", delete_users),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
