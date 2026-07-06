from django.contrib.auth.models import AbstractUser
from django.db import models


class AdvancedUser(AbstractUser):
    # 1. Переопределяем поле email, делая его уникальным (unique=True) и обязательным
    email = models.EmailField(unique=True, verbose_name="Электронная почта")

    # Дополнительное кастомное поле (например, для телефона)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")

    # 2. Указываем Django, что ТЕПЕРЬ главным полем для логина будет 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email