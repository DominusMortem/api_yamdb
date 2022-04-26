from rest_framework import viewsets, permissions, filters
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from titles.models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

