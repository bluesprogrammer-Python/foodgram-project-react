from django.shortcuts import render

from rest_framework import viewsets
from .serializers import UserSerializers
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers