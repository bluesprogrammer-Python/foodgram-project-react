from django.shortcuts import render

from djoser.views import UserViewSet
from .serializers import UserSerializers
from .models import User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers