from rest_framework import viewsets, permissions, filters, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.core.mail import EmailMessage

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from titles.models import User
from .serializers import UserSerializer, MyTokenObtainSerializer
from rest_framework.renderers import JSONRenderer


def send_email(data, uid64):
    email = EmailMessage(
        'Authorization',
        f"Имя пользователя: {data['username']}"
        f"Код подтверждения: {uid64}",
        data['email'],
        ['email']
    )
    email.send()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = User.objects.get(username=serializer.data['username'])
        uid64 = urlsafe_base64_encode(force_bytes(f'{user.pk}/{user}'))
        send_email(serializer.data, uid64)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer

