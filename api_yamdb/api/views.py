from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.core.mail import EmailMessage
from rest_framework.pagination import PageNumberPagination
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from titles.models import User
from .serializers import UserSerializer, MyTokenObtainSerializer
from .mixins import CreateViewSet
from .permissions import IsAdmin


def send_email(user, uid64):
    email = EmailMessage(
        'Authorization',
        f"Имя пользователя: {user}\n"
        f"Код подтверждения: {uid64}",
        'admin@mail.fake',
        [user.email]
    )
    email.send()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'me':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get', 'patch', 'delete'])
    def me(self, request):
        if request.method not in ['GET', 'PATCH']:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        if not token:
            return Response({'token': 'Отсутствует токен.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user = User.objects.get(pk=valid_data['user_id'])
            if request.method == 'GET':
                serializer = self.get_serializer(user, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.method == 'PATCH':
                username = request.data.get('username', False)
                email = request.data.get('email', False)
                if username != user.username and User.objects.filter(username=username).exists():
                    return Response({"username": 'Никнейм занят.'})
                if email != user.email and User.objects.filter(email=email).exists():
                    return Response({"email": 'Емейл занят.'})
                if user.role == 'user' and request.data.get('role', False):
                    data = dict(request.data)
                    data['role'] = 'user'
                    serializer = self.get_serializer(user, data=data, partial={'username': username})
                else:
                    serializer = self.get_serializer(user, data=request.data, partial={'username': username})
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
        except ValidationError as v:
            return Response({"validation error": v})


class SignUpViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        if request.data.get("username", False) == 'me':
            return Response(
                {'username': 'Такое имя создать нельзя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            username = request.data.get("username", False)
            email = request.data.get('email', False)
            user = User.objects.get(username=username, email=email)
            data = dict()
            if not username:
                data['username'] = ['Обязательное поле']
            if not email:
                data['email'] = ['Обязательное поле']
            if dict():
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except self.queryset.model.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
        uid64 = urlsafe_base64_encode(force_bytes(f'{user.pk}/{user}'))
        send_email(user, uid64)
        return Response(request.data, status=status.HTTP_200_OK)


class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer
