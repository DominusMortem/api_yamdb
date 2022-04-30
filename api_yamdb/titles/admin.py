from django.contrib import admin

from .models import User

# Регистрация модели пользователя в админке
admin.site.register(User)