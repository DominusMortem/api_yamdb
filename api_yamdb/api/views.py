from rest_framework import viewsets, permissions, filters
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from titles.models import User
from .serializers import UserSerializer, MyTokenObtainSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer