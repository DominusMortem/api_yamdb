from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueTogetherValidator

from titles.models import User


class BadConfirmationCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Wrong confirmation code.')
    default_code = 'Wrong confirmation code'


def send_email(validated_data):
    email = EmailMessage(
        'Регистрационные данные',
        f"Имя пользователя: {validated_data['username']}",
        validated_data['email'],
        ['email']
    )
    email.send()


def authenticate(uid, user):
    try:
        uid_decode = urlsafe_base64_decode(uid)
        username = user
        user_id = user.id
        if uid_decode.decode('utf-8') == f'{user_id}/{username}':
            return True
    except ValueError:
        False
    else:
        return False


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        read_only_fields = ('role',)


class MyTokenObtainSerializer(TokenObtainSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        uid = attrs['confirmation_code']
        self.user = User.objects.get(username=attrs[self.username_field])
        data = dict()
        if authenticate(uid, self.user):
            refresh = self.get_token(self.user)
            data['token'] = str(refresh.access_token)
        else:
            raise BadConfirmationCode(
                'Проверочный код недействителен.'
            )
        return data


