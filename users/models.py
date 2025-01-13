from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Укажите ваш email"
    )
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="Аватар", blank=True, null=True
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        help_text="Укажите номер телефона",
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        help_text="Укажите страну",
        blank=True,
        null=True,
    )
    telegram_id = models.CharField(
        max_length=100,
        verbose_name="ID Telegram",
        help_text="Укажите ID Telegram",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
