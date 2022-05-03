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
        default='user'
    )

    class Meta:
        ordering = ('-pk',)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pk',)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pk',)


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(Category,
                                 on_delete=models.DO_NOTHING,
                                 related_name='category')
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through='TitleGenre')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pk',)


class TitleGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.FloatField()
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review')
        ]
        ordering = ('-pk',)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-pk',)
