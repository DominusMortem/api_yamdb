from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

CHOICES_ROLE = (('user', 'Пользователь'),
                ('moderator', 'Модератор'),
                ('admin', 'Администратор'))


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
                  max_length=10,
                  choices=CHOICES_ROLE,
                  default='user')
