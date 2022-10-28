from django.urls import path
from rest_framework.authtoken import views

from .views import UserCreateAPIView

urlpatterns = [
    path("api-token-auth/", views.obtain_auth_token),
    path("user_create/", UserCreateAPIView.as_view()),
]
