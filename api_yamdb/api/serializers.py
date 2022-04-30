from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _


from titles.models import User, Category, Comment, Genre, Review, Title


class BadConfirmationCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Wrong confirmation code.')
    default_code = 'Wrong confirmation code'


def authenticate(uid, user):
    try:
        uid_decode = urlsafe_base64_decode(uid)
        username = user
        user_id = user.id
        if uid_decode.decode('utf-8') == f'{user_id}/{username}':
            return True
    except ValueError:
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
        self.user = get_object_or_404(User, username=attrs[self.username_field])
        data = dict()
        if authenticate(uid, self.user):
            refresh = self.get_token(self.user)
            data['token'] = str(refresh.access_token)
        else:
            raise BadConfirmationCode(
                'Проверочный код недействителен.'
            )
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ['author', 'title']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ['author', 'review']


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre', 'description')
