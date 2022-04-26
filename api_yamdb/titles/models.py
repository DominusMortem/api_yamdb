from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES_ROLE = (('users', 'Пользователь'),
                ('moderators', 'Модератор'),
                ('admin', 'Администратор'))


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
                  max_length=10,
                  choices=CHOICES_ROLE,
                  default='users')