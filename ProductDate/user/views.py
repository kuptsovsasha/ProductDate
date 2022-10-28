from rest_framework import generics, permissions

from .models import User
from .serializers import UserCreateSerializer


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserCreateSerializer
